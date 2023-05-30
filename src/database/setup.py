"""
Utility functions for initializing the database and tables through SQLAlchemy.
"""
from typing import List

from connectors.resource_with_relations import ResourceWithRelations
from database.model import AIAsset
from database.model.dataset import Dataset
from sqlalchemy import text, and_
from sqlalchemy.engine import Engine
from sqlmodel import create_engine, Session, select

from connectors import ResourceConnector
from database.model.publication import Publication
from database.model.resource import Resource
from platform_names import PlatformName


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
        Resource.metadata.create_all(connection, checkfirst=True)
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
            session.scalars(select(Publication)).first() or session.scalars(select(Dataset)).first()
        )
        if only_if_empty and data_exists:
            return

        for connector in connectors:
            for item in connector.fetch_all(limit=limit):
                if isinstance(item, ResourceWithRelations):
                    resource = item.resource
                    _create_or_fetch_related_objects(session, item.related_resources)
                else:
                    resource = item
                if _get_existing_resource(session, resource) is None:
                    asset = AIAsset(type=resource.__tablename__)
                    session.add(asset)
                    session.flush()
                    resource.identifier = asset.identifier
                    session.add(resource)
                if isinstance(item, ResourceWithRelations):
                    _link_resource_with_relations(item)
                session.flush()
        session.commit()


def _link_resource_with_relations(item: ResourceWithRelations):
    """
    Set the relationship from `item.resource` to the `item.related_resources`.
    This should be performed after all resources have been inserted in the database.
    """
    for field_name, related_resource_or_list in item.related_resources.items():
        if isinstance(related_resource_or_list, Resource):
            resource: Resource = related_resource_or_list
            item.resource.__setattr__(field_name, resource)
        else:
            resources: list[Resource] = related_resource_or_list
            item.resource.__setattr__(field_name, resources)


def _get_existing_resource(session: Session, resource: Resource) -> Resource | None:
    """Selecting a resource based on platform and platform_identifier"""
    clazz = type(resource)
    query = select(clazz).where(
        and_(
            clazz.platform == resource.platform,
            clazz.platform_identifier == resource.platform_identifier,
        )
    )
    return session.scalars(query).first()


def _create_or_fetch_related_objects(
    session: Session, related_resources: dict[str, Resource | List[Resource]]
):
    """
    For all resources in the `related_resources`, make sure they have an identifier, by either
    inserting them in the database, or retrieving the existing values.
    """
    for related_resource_or_list in related_resources.values():
        resources: list[Resource] = []
        if isinstance(related_resource_or_list, Resource):
            resources = [related_resource_or_list]
        else:
            resources = related_resource_or_list
        for resource in resources:
            if (
                resource.platform is not None
                and resource.platform != PlatformName.aiod
                and resource.platform_identifier is not None
            ):
                existing = _get_existing_resource(session, resource)
                if existing is None:
                    asset = AIAsset(type=resource.__tablename__)
                    session.add(asset)
                    session.flush()
                    resource.identifier = asset.identifier
                    session.add(resource)
                else:
                    resource.identifier = existing.identifier
