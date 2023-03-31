"""
Utility functions for initializing the database and tables through SQLAlchemy.
"""
from typing import List

from sqlalchemy import Engine, text, create_engine, select
from sqlalchemy.orm import Session

import converters
from connectors import ResourceConnector
from connectors.resource_with_relations import ResourceWithRelations
from schemas import AIoDAIResource
from .model.ai_resource import OrmAIResource
from .model.base import Base  # noqa:F401
from .model.dataset import OrmDataset
from .model.publication import OrmPublication


def connect_to_database(
    url: str = "mysql://root:ok@127.0.0.1:3307/aiod",
    create_if_not_exists: bool = True,
    delete_first: bool = False,
) -> Engine:
    """Connect to server, optionally creating the database if it does not exist.

    Params
    ------
    url: URL to the database, see https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls # noqa
    create_if_not_exists: create the database if it does not exist
    delete_first: drop the database before creating it again, to start with an empty database.
        IMPORTANT: Using `delete_first` means ALL data in that database will be lost permanently.

    Returns
    -------
    engine: Engine SQLAlchemy Engine configured with a database connection
    """

    if delete_first or create_if_not_exists:
        drop_or_create_database(url, delete_first)
    engine = create_engine(url, echo=True, pool_recycle=3600)

    with engine.connect() as connection:
        Base.metadata.create_all(connection, checkfirst=True)
        connection.commit()
    return engine


def drop_or_create_database(url: str, delete_first: bool):
    server, database = url.rsplit("/", 1)
    engine = create_engine(server, echo=True)  # Temporary engine, not connected to a database

    with engine.connect() as connection:
        if delete_first:
            connection.execute(text(f"DROP DATABASE IF EXISTS {database}"))
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        connection.commit()
    engine.dispose()


def populate_database(
    engine: Engine,
    connectors: List[ResourceConnector],
    only_if_empty: bool = True,
    limit: int | None = None,
):
    """Add some data to the Dataset and Publication tables."""

    with Session(engine) as session:
        data_exists = (
            session.scalars(select(OrmPublication)).first()
            or session.scalars(select(OrmDataset)).first()
        )
        if only_if_empty and data_exists:
            return

        for connector in connectors:
            for item in connector.fetch_all(limit=limit):
                if isinstance(item, ResourceWithRelations):
                    orm_resource = _convert(session, item.resource)
                    _add_related_objects(session, orm_resource, item.related_resources)
                else:
                    orm_resource = _convert(session, item)
                session.add(orm_resource)
        session.commit()


def _add_related_objects(
    session: Session,
    orm_resource: OrmAIResource,
    related_resources: dict[str, AIoDAIResource | List[AIoDAIResource]],
):
    for field_name, related_resource_or_list in related_resources.items():
        if isinstance(related_resource_or_list, AIoDAIResource):
            resource: AIoDAIResource = related_resource_or_list
            related_orm = _convert(session, resource)
            orm_resource.__setattr__(field_name, related_orm)
        else:
            resources: list[AIoDAIResource] = related_resource_or_list
            related_orms = [_convert(session, resource) for resource in resources]
            orm_resource.__setattr__(field_name, related_orms)


def _convert(session: Session, resource: AIoDAIResource) -> OrmAIResource:
    converter = converters.converters[type(resource)]
    return converter.aiod_to_orm(session, resource, return_existing_if_present=True)
