"""
Defines Rest API endpoints.

Note: order matters for overloaded paths
(https://fastapi.tiangolo.com/tutorial/path-params/#order-matters).
"""
import argparse
import os
import tomllib
import traceback
from typing import Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Json
from sqlalchemy import select, Engine, and_, delete, update
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

import connectors
import schemas
from authentication import get_current_user
from connectors import NodeName
from converters import dataset_converter
from database.model.educational_resource import OrmEducationalResource
from database.model.base import (
    OrmBusinessCategory,
    OrmLanguage,
    OrmTag,
    OrmTargetAudience,
    OrmTechnicalCategory,
)
from database.model.news import OrmNews, OrmNewsCategory
from database.model.dataset import OrmDataset
from database.model.publication import OrmPublication
from database.setup import connect_to_database, populate_database


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Please refer to the README.")
    parser.add_argument("--url-prefix", default="", help="Prefix for the api url.")
    parser.add_argument(
        "--rebuild-db",
        default="only-if-empty",
        choices=["no", "only-if-empty", "always"],
        help="Determines if the database is recreated.",
    )
    parser.add_argument(
        "--populate-datasets",
        default=[],
        nargs="+",
        choices=[p.name for p in NodeName],
        help="Zero, one or more nodes with which the datasets should get populated.",
    )
    parser.add_argument(
        "--populate-publications",
        default=[],
        nargs="+",
        choices=[p.name for p in NodeName],
        help="Zero, one or more nodes with which the publications should get populated.",
    )
    parser.add_argument(
        "--limit-number-of-datasets",
        type=int,
        default=None,
        help="Limit the number of initial datasets with which the database is populated, per node.",
    )
    parser.add_argument(
        "--limit-number-of-publications",
        default=None,
        type=int,
        help="Limit the number of initial publication with which the database is populated, "
        "per node.",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Use `--reload` for FastAPI.",
    )
    return parser.parse_args()


def _engine(rebuild_db: str) -> Engine:
    """
    Return a SqlAlchemy engine, backed by the MySql connection as configured in the configuration
    file.
    """
    with open("config.toml", "rb") as fh:
        config = tomllib.load(fh)
    db_config = config.get("database", {})
    username = db_config.get("name", "root")
    password = db_config.get("password", "ok")
    host = db_config.get("host", "demodb")
    port = db_config.get("port", 3306)
    database = db_config.get("database", "aiod")

    db_url = f"mysql://{username}:{password}@{host}:{port}/{database}"

    delete_before_create = rebuild_db == "always"
    return connect_to_database(db_url, delete_first=delete_before_create)


def _connector_from_node_name(connector_type: str, connector_dict: Dict, node_name: str):
    """Get the connector from the connector_dict, identified by its node name."""
    try:
        node = NodeName(node_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Node '{node_name}' not recognized.")
    connector = connector_dict.get(node, None)
    if connector is None:
        possibilities = ", ".join(f"`{c}`" for c in connectors.dataset_connectors.keys())
        msg = (
            f"No {connector_type} connector for node '{node_name}' available. Possible values:"
            f" {possibilities}"
        )
        raise HTTPException(status_code=501, detail=msg)
    return connector


def _retrieve_dataset(session, identifier, node=None) -> OrmDataset:
    if node is None:
        query = select(OrmDataset).where(OrmDataset.id == identifier)
    else:
        if node not in {n.name for n in NodeName}:
            raise HTTPException(status_code=400, detail=f"Node '{node}' not recognized.")
        query = select(OrmDataset).where(
            and_(
                OrmDataset.node_specific_identifier == identifier,
                OrmDataset.node == node,
            )
        )
    dataset = session.scalars(query).first()
    if not dataset:
        if node is None:
            msg = f"Dataset '{identifier}' not found in the database."
        else:
            msg = f"Dataset '{identifier}' of '{node}' not found in the database."
        raise HTTPException(status_code=404, detail=msg)
    return dataset


def _retrieve_publication(session, identifier) -> OrmPublication:
    query = select(OrmPublication).where(OrmPublication.id == identifier)
    publication = session.scalars(query).first()
    if not publication:
        raise HTTPException(
            status_code=404,
            detail=f"Publication '{identifier}' not found in the database.",
        )
    return publication


def _retrieve_news(session, identifier) -> OrmNews:
    query = select(OrmNews).where(OrmNews.id == identifier)
    news = session.scalars(query).first()
    if not news:
        raise HTTPException(
            status_code=404,
            detail=f"News '{identifier}' not found in the database.",
        )
    return news


def _retrieve_educational_resource(session, identifier) -> OrmEducationalResource:
    query = select(OrmEducationalResource).where(OrmEducationalResource.id == identifier)
    news = session.scalars(query).first()
    if not news:
        raise HTTPException(
            status_code=404,
            detail=f"Educational resource '{identifier}' not found in the database.",
        )
    return news


def _wrap_as_http_exception(exception: Exception) -> HTTPException:
    if isinstance(exception, HTTPException):
        return exception

    # This is an unexpected error. A mistake on our part. End users should not be informed about
    # details of problems they are not expected to fix, so we give a generic response and log the
    # error.
    traceback.print_exc()
    return HTTPException(
        status_code=500,
        detail=(
            "Unexpected exception while processing your request. Please contact the maintainers."
        ),
    )


def add_routes(app: FastAPI, engine: Engine, url_prefix=""):
    """Add routes to the FastAPI application"""

    @app.get(url_prefix + "/", response_class=HTMLResponse)
    def home() -> str:
        """Provides a redirect page to the docs."""
        return """
        <!DOCTYPE html>
        <html>
          <head>
            <meta http-equiv="refresh" content="0; url='docs'" />
          </head>
          <body>
            <p>The REST API documentation is <a href="docs">here</a>.</p>
          </body>
        </html>
        """

    # Multiple endpoints share the same set of parameters, we define a class for easy re-use of
    # dependencies:
    # https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/?h=depends#classes-as-dependencies # noqa
    class Pagination(BaseModel):
        offset: int = 0
        limit: int = 100

    @app.get(url_prefix + "/authorization_test")
    def test_authorization(user: Json = Depends(get_current_user)) -> dict:
        """
        Returns the user, if authenticated correctly.
        """
        return {"msg": "success", "user": user}

    @app.get(url_prefix + "/datasets/", response_model_exclude_none=True)
    def list_datasets(
        pagination: Pagination = Depends(Pagination),
    ) -> list[schemas.AIoDDataset]:
        """Lists all datasets registered with AIoD.

        Query Parameter
        ------
         * nodes, list[str], optional: if provided, list only datasets from the given node.
        """
        # For additional information on querying through SQLAlchemy's ORM:
        # https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
        try:
            with Session(engine) as session:
                query = select(OrmDataset).offset(pagination.offset).limit(pagination.limit)
                return [
                    dataset_converter.orm_to_aiod(dataset)
                    for dataset in session.scalars(query).all()
                ]
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/datasets/{identifier}", response_model_exclude_none=True)
    def get_dataset(identifier: str) -> schemas.AIoDDataset:
        """Retrieve all meta-data for a specific dataset."""
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, identifier)
                return dataset_converter.orm_to_aiod(dataset)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/nodes")
    def get_nodes() -> list:
        """Retrieve information about all known nodes"""
        return list(NodeName)

    @app.get(url_prefix + "/nodes/{node}/datasets", response_model_exclude_none=True)
    def get_node_datasets(
        node: str, pagination: Pagination = Depends(Pagination)
    ) -> list[schemas.AIoDDataset]:
        """Retrieve all meta-data of the datasets of a single node."""
        try:
            with Session(engine) as session:
                query = (
                    select(OrmDataset)
                    .where(OrmDataset.node == node)
                    .offset(pagination.offset)
                    .limit(pagination.limit)
                )
                return [
                    dataset_converter.orm_to_aiod(dataset)
                    for dataset in session.scalars(query).all()
                ]
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/nodes/{node}/datasets/{identifier}", response_model_exclude_none=True)
    def get_node_dataset(node: str, identifier: str) -> schemas.AIoDDataset:
        """Retrieve all meta-data for a specific dataset identified by the
        node-specific-identifier."""
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, identifier, node)
                return dataset_converter.orm_to_aiod(dataset)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.post(url_prefix + "/datasets/", response_model_exclude_none=True)
    def register_dataset(dataset: schemas.AIoDDataset) -> schemas.AIoDDataset:
        """Register a dataset with AIoD."""
        try:
            with Session(engine) as session:
                dataset_orm = dataset_converter.aiod_to_orm(session, dataset)
                session.add(dataset_orm)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    query = select(OrmDataset).where(
                        and_(
                            OrmDataset.node == dataset.node,
                            OrmDataset.name == dataset.name,
                        )
                    )
                    existing_dataset = session.scalars(query).first()
                    raise HTTPException(
                        status_code=409,
                        detail="There already exists a dataset with the same "
                        f"node and name, with id={existing_dataset.id}.",
                    )
                return dataset_converter.orm_to_aiod(dataset_orm)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.put(url_prefix + "/datasets/{identifier}", response_model_exclude_none=True)
    def put_dataset(identifier: str, dataset: schemas.AIoDDataset) -> schemas.AIoDDataset:
        """Update an existing dataset."""
        try:
            with Session(engine) as session:
                _retrieve_dataset(session, identifier)  # Raise error if it does not exist
                dataset_orm = dataset_converter.aiod_to_orm(session, dataset)
                dataset_orm.id = identifier
                session.merge(dataset_orm)
                session.commit()
                new_dataset = _retrieve_dataset(session, identifier)
                return dataset_converter.orm_to_aiod(new_dataset)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.delete(url_prefix + "/datasets/{identifier}")
    def delete_dataset(identifier: str):
        try:
            with Session(engine) as session:
                _retrieve_dataset(session, identifier)  # Raise error if it does not exist

                statement = delete(OrmDataset).where(OrmDataset.id == identifier)
                session.execute(statement)
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/publications")
    def list_publications(pagination: Pagination = Depends(Pagination)) -> list[dict]:
        """Lists all publications registered with AIoD."""
        try:
            with Session(engine) as session:
                return [
                    publication.to_dict(depth=0)
                    for publication in session.scalars(
                        select(OrmPublication).offset(pagination.offset).limit(pagination.limit)
                    ).all()
                ]
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.post(url_prefix + "/publications")
    def register_publication(publication: schemas.AIoDPublication) -> dict:
        """Add a publication."""
        try:
            with Session(engine) as session:
                new_publication = OrmPublication(title=publication.title, url=publication.url)
                session.add(new_publication)
                session.commit()
                return new_publication.to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/publications/{identifier}")
    def get_publication(identifier: str) -> dict:
        """Retrieves all information for a specific publication registered with AIoD."""
        try:
            with Session(engine) as session:
                publication = _retrieve_publication(session, identifier)
                return publication.to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.put(url_prefix + "/publications/{identifier}")
    def update_publication(identifier: str, publication: schemas.AIoDPublication) -> dict:
        """Update this publication"""
        try:
            with Session(engine) as session:
                _retrieve_publication(session, identifier)  # Raise error if dataset does not exist
                statement = (
                    update(OrmPublication)
                    .values(
                        title=publication.title,
                        url=publication.url,
                    )
                    .where(OrmPublication.id == identifier)
                )
                session.execute(statement)
                session.commit()
                return _retrieve_publication(session, identifier).to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.delete(url_prefix + "/publications/{identifier}")
    def delete_publication(identifier: str):
        """Delete this publication from AIoD."""
        try:
            with Session(engine) as session:
                _retrieve_publication(session, identifier)  # Raise error if it does not exist

                statement = delete(OrmPublication).where(OrmPublication.id == identifier)
                session.execute(statement)
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/datasets/{identifier}/publications")
    def list_publications_related_to_dataset(identifier: str) -> list[dict]:
        """Lists all publications registered with AIoD that use this dataset."""
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, identifier)
                return [publication.to_dict(depth=0) for publication in dataset.citations]
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.post(url_prefix + "/datasets/{dataset_id}/publications/{publication_id}")
    def relate_publication_to_dataset(dataset_id: str, publication_id: str):
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, dataset_id)
                publication = _retrieve_publication(session, publication_id)
                if publication in dataset.citations:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Dataset {dataset_id} is already linked to publication "
                        f"{publication_id}.",
                    )
                dataset.citations.append(publication)
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.delete(url_prefix + "/datasets/{dataset_id}/publications/{publication_id}")
    def delete_relation_publication_to_dataset(dataset_id: str, publication_id: str):
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, dataset_id)
                publication = _retrieve_publication(session, publication_id)
                if publication not in dataset.citations:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Dataset {dataset_id} is not linked to publication "
                        f"{publication_id}.",
                    )
                dataset.citations = [p for p in dataset.citations if p != publication]
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.post(url_prefix + "/news")
    def register_news(news: schemas.News) -> dict:
        """Add news."""
        try:
            with Session(engine) as session:
                tags = []
                if news.tags:
                    for t in news.tags:
                        query = select(OrmTag).where(OrmTag.tag == t)
                        tag = session.scalars(query).first()
                        if not tag:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Tag '{t}' not found in the database.",
                            )
                        tags.append(tag)

                business_categories = []
                if news.business_categories:
                    for c in news.business_categories:
                        query = select(OrmBusinessCategory).where(OrmBusinessCategory.category == c)
                        category = session.scalars(query).first()
                        if not category:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Business category '{c}' not found in the database.",
                            )
                        business_categories.append(category)
                news_categories = []
                if news.news_categories:
                    for c in news.news_categories:
                        query = select(OrmNewsCategory).where(OrmNewsCategory.category == c)
                        category = session.scalars(query).first()
                        if not category:
                            raise HTTPException(
                                status_code=404,
                                detail=f"News category '{c}' not found in the database.",
                            )
                        news_categories.append(category)

                new_news = OrmNews(
                    title=news.title,
                    date_modified=news.date_modified,
                    body=news.body,
                    source=news.source,
                    headline=news.headline,
                    alternative_headline=news.alternative_headline,
                    section=news.section,
                    word_count=news.word_count,
                )

                new_news.tags = tags
                new_news.business_categories = business_categories
                new_news.news_categories = news_categories
                session.add(new_news)
                try:
                    session.commit()
                except (OperationalError, IntegrityError):
                    session.rollback()
                    raise HTTPException(
                        status_code=422,
                        detail="Missing required non null values",
                    )

                return new_news.to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/news")
    def list_all_news(pagination: Pagination = Depends(Pagination)) -> list[schemas.News]:
        """Lists all news registered with AIoD."""
        try:
            with Session(engine) as session:
                query = select(OrmNews).offset(pagination.offset).limit(pagination.limit)
                return session.scalars(query).all()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/news/{identifier}")
    def get_news(identifier: str) -> dict:
        """Retrieve all meta-data for specific news entity."""
        try:
            with Session(engine) as session:
                news = _retrieve_news(session, identifier)
                return news
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.delete(url_prefix + "/news/{identifier}")
    def delete_news(identifier: str):
        """Delete this news from AIoD."""
        try:
            with Session(engine) as session:
                _retrieve_news(session, identifier)  # Raise error if it does not exist

                statement = delete(OrmNews).where(OrmNews.id == identifier)
                session.execute(statement)
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.put(url_prefix + "/news/{identifier}")
    def put_news(identifier: str, news: schemas.News) -> dict:
        """Update existing news."""
        try:
            with Session(engine) as session:
                _retrieve_news(session, identifier)  # Raise error if dataset does not exist
                statement = (
                    update(OrmNews)
                    .values(
                        title=news.title,
                        date_modified=news.date_modified,
                        body=news.body,
                        source=news.source,
                        headline=news.headline,
                        alternative_headline=news.alternative_headline,
                        section=news.section,
                        word_count=news.word_count,
                    )
                    .where(OrmNews.id == identifier)
                )
                # TODO update categories (business,news) and tags
                session.execute(statement)
                session.commit()
                return _retrieve_news(session, identifier).to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.post(url_prefix + "/educational_resource")
    def register_educational_resource(educational_resource: schemas.EducationalResource) -> dict:
        """Add educational resource."""
        try:
            with Session(engine) as session:
                tags = []
                if educational_resource.tags:
                    for t in educational_resource.tags:
                        query = select(OrmTag).where(OrmTag.tag == t)
                        tag = session.scalars(query).first()
                        if not tag:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Tag '{t}' not found in the database.",
                            )
                        tags.append(tag)

                business_categories = []
                if educational_resource.business_categories:
                    for c in educational_resource.business_categories:
                        query = select(OrmBusinessCategory).where(OrmBusinessCategory.category == c)
                        category = session.scalars(query).first()
                        if not category:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Business category '{c}' not found in the database.",
                            )
                        business_categories.append(category)

                technical_categories = []
                if educational_resource.technical_categories:
                    for c in educational_resource.technical_categories:
                        query = select(OrmTechnicalCategory).where(
                            OrmTechnicalCategory.category == c
                        )
                        category = session.scalars(query).first()
                        if not category:
                            raise HTTPException(
                                status_code=404,
                                detail=f"News category '{c}' not found in the database.",
                            )
                        technical_categories.append(category)
                target_audience = []
                if educational_resource.target_audience:
                    for a in educational_resource.target_audience:
                        query = select(OrmTargetAudience).where(OrmTargetAudience.audience == a)
                        audience = session.scalars(query).first()
                        if not audience:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Target audience '{a}' not found in the database.",
                            )
                        target_audience.append(audience)
                languages = []
                if educational_resource.languages:
                    for la in educational_resource.languages:
                        query = select(OrmLanguage).where(OrmLanguage.language == la)
                        language = session.scalars(query).first()
                        if not language:
                            raise HTTPException(
                                status_code=404,
                                detail=f"language '{la}' not found in the database.",
                            )
                        languages.append(language)

                new_educational_resource = OrmEducationalResource(
                    title=educational_resource.title,
                    date_modified=educational_resource.date_modified,
                    body=educational_resource.body,
                    website_url=educational_resource.website_url,
                    educational_role=educational_resource.educational_role,
                    educational_level=educational_resource.educational_level,
                    educatonal_type=educational_resource.educatonal_type,
                    interactivity_type=educational_resource.interactivity_type,
                    accessibility_api=educational_resource.accessibility_api,
                    accessibility_control=educational_resource.accessibility_control,
                    access_mode=educational_resource.access_mode,
                    access_mode_sufficient=educational_resource.access_mode_sufficient,
                    access_restrictions=educational_resource.access_restrictions,
                    citation=educational_resource.citation,
                    typical_age_range=educational_resource.typical_age_range,
                    version=educational_resource.version,
                    number_of_weeks=educational_resource.number_of_weeks,
                    credits=educational_resource.credits,
                    field_prerequisites=educational_resource.field_prerequisites,
                    short_summary=educational_resource.short_summary,
                    duration_minutes_and_hours=educational_resource.duration_minutes_and_hours,
                    hours_per_week=educational_resource.hours_per_week,
                    country=educational_resource.country,
                    is_accessible_for_free=educational_resource.is_accessible_for_free,
                    duration_in_years=educational_resource.duration_in_years,
                    pace=educational_resource.pace,
                    time_required=educational_resource.time_required,
                )

                new_educational_resource.tags = tags
                new_educational_resource.business_categories = business_categories
                new_educational_resource.technical_categories = technical_categories
                new_educational_resource.target_audience = target_audience
                new_educational_resource.languages = languages
                session.add(new_educational_resource)
                try:
                    session.commit()
                except (OperationalError, IntegrityError):
                    session.rollback()
                    raise HTTPException(
                        status_code=422,
                        detail="Missing required non null values",
                    )
                return new_educational_resource.to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/educational_resource")
    def list_all_educational_resources(
        pagination: Pagination = Depends(Pagination),
    ) -> list[schemas.EducationalResource]:
        """Lists all educational resources registered with AIoD."""
        try:
            with Session(engine) as session:
                query = (
                    select(OrmEducationalResource).offset(pagination.offset).limit(pagination.limit)
                )
                return session.scalars(query).all()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.get(url_prefix + "/educational_resource/{identifier}")
    def get_educational_resource(identifier: str) -> dict:
        """Retrieve all meta-data for specific educational resource entity."""
        try:
            with Session(engine) as session:
                educational_resource = _retrieve_educational_resource(session, identifier)
                return educational_resource
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.delete(url_prefix + "/educational_resource/{identifier}")
    def delete_educational_resource(identifier: str):
        """Delete this educational resource from AIoD."""
        try:
            with Session(engine) as session:
                _retrieve_educational_resource(
                    session, identifier
                )  # Raise error if it does not exist

                statement = delete(OrmEducationalResource).where(
                    OrmEducationalResource.id == identifier
                )
                session.execute(statement)
                session.commit()
        except Exception as e:
            raise _wrap_as_http_exception(e)

    @app.put(url_prefix + "/educational_resource/{identifier}")
    def put_educational_resource(
        identifier: str, educational_resource: schemas.EducationalResource
    ) -> dict:
        """Update existing educational resource."""
        try:
            with Session(engine) as session:
                _retrieve_news(session, identifier)  # Raise error if dataset does not exist
                statement = (
                    update(OrmEducationalResource)
                    .values(
                        title=educational_resource.title,
                        date_modified=educational_resource.date_modified,
                        body=educational_resource.body,
                        website_url=educational_resource.website_url,
                        educational_role=educational_resource.educational_role,
                        educational_level=educational_resource.educational_level,
                        educatonal_type=educational_resource.educatonal_type,
                        interactivity_type=educational_resource.interactivity_type,
                        accessibility_api=educational_resource.accessibility_api,
                        accessibility_control=educational_resource.accessibility_control,
                        access_mode=educational_resource.access_mode,
                        access_restrictions=educational_resource.access_restrictions,
                        citation=educational_resource.citation,
                        version=educational_resource.version,
                        field_prerequisites=educational_resource.field_prerequisites,
                        short_summary=educational_resource.short_summary,
                        duration_minutes_and_hours=educational_resource.duration_minutes_and_hours,
                        hours_per_week=educational_resource.hours_per_week,
                        country=educational_resource.country,
                        is_accessible_for_free=educational_resource.is_accessible_for_free,
                        duration_in_years=educational_resource.duration_in_years,
                        pace=educational_resource.pace,
                        time_required=educational_resource.time_required,
                    )
                    .where(OrmEducationalResource.id == identifier)
                )
                # TODO update categories (business,news) and tags
                session.execute(statement)
                session.commit()
                return _retrieve_educational_resource(session, identifier).to_dict(depth=1)
        except Exception as e:
            raise _wrap_as_http_exception(e)


def create_app() -> FastAPI:
    """Create the FastAPI application, complete with routes."""
    app = FastAPI(
        swagger_ui_init_oauth={
            "clientId": os.getenv("KEYCLOAK_CLIENT_ID"),
            "clientSecret": os.getenv("KEYCLOAK_CLIENT_SECRET"),
            "realm": "dev",
            "appName": "AIoD API",
            "usePkceWithAuthorizationCodeGrant": True,
            "scopes": "openid profile",
        }
    )
    args = _parse_args()

    dataset_connectors = [
        _connector_from_node_name("dataset", connectors.dataset_connectors, node_name)
        for node_name in args.populate_datasets
    ]
    publication_connectors = [
        _connector_from_node_name("publication", connectors.publication_connectors, node_name)
        for node_name in args.populate_publications
    ]
    engine = _engine(args.rebuild_db)
    if len(dataset_connectors) + len(publication_connectors) > 0:
        populate_database(
            engine,
            dataset_connectors=dataset_connectors,
            publications_connectors=publication_connectors,
            only_if_empty=True,
            limit_datasets=args.limit_number_of_datasets,
            limit_publications=args.limit_number_of_publications,
        )
    add_routes(app, engine, url_prefix=args.url_prefix)
    return app


def main():
    """Run the application. Placed in a separate function, to avoid having global variables"""
    args = _parse_args()
    load_dotenv()
    uvicorn.run("main:create_app", host="0.0.0.0", reload=args.reload, factory=True)


if __name__ == "__main__":
    main()
