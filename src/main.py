"""
Defines Rest API endpoints.

Note: order matters for overloaded paths
(https://fastapi.tiangolo.com/tutorial/path-params/#order-matters).
"""
import argparse
import tomllib
import traceback
from typing import Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select, Engine, and_
from sqlalchemy.orm import Session

import connectors
import routers
from connectors import NodeName
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


def _retrieve_publication(session, identifier, node=None) -> OrmPublication:
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
    publication = session.scalars(query).first()
    if not publication:
        if node is None:
            msg = f"Publication '{identifier}' not found in the database."
        else:
            msg = f"Publication '{identifier}' of '{node}' not found in the database."
        raise HTTPException(status_code=404, detail=msg)
    return publication


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
    for router in routers.routers:
        app.include_router(router.add_routes(engine, url_prefix))

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

    @app.get(url_prefix + "/nodes")
    def get_nodes() -> list:
        """Retrieve information about all known nodes"""
        return list(NodeName)

    @app.get(url_prefix + "/datasets/{identifier}/publications")
    def list_publications_related_to_dataset(identifier: str) -> list[dict]:
        """Lists all publications registered with AIoD that use this dataset."""
        try:
            with Session(engine) as session:
                dataset = _retrieve_dataset(session, identifier)
                return [publication.to_dict(depth=0) for publication in dataset.citations]
        except Exception as e:
            raise _wrap_as_http_exception(e)


def create_app() -> FastAPI:
    """Create the FastAPI application, complete with routes."""
    app = FastAPI()
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
    uvicorn.run("main:create_app", host="0.0.0.0", reload=args.reload, factory=True)


if __name__ == "__main__":
    main()
