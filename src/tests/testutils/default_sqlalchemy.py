import tempfile
from typing import Iterator

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine, Engine, insert
from starlette.testclient import TestClient

from database.model.base import Base
from main import add_routes
from tests.testutils.test_resource import OrmTestResource, RouterTestResource


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """
    Create a SqlAlchemy engine for tests, backed by a temporary sqlite file.
    """
    temporary_file = tempfile.NamedTemporaryFile()
    engine = create_engine(f"sqlite:///{temporary_file.name}")
    Base.metadata.create_all(engine)
    # Yielding is essential, the temporary file will be closed after the engine is used
    yield engine


@pytest.fixture(scope="session")
def engine_with_test_resource() -> Iterator[Engine]:
    """Create a SqlAlchemy Engine populated with an instance of the TestResource"""
    temporary_file = tempfile.NamedTemporaryFile()
    engine = create_engine(f"sqlite:///{temporary_file.name}")
    OrmTestResource.metadata.create_all(engine)
    yield engine


@pytest.fixture(autouse=True)
def clear_db(request):
    """
    This fixture will be used by every test and checks if the test uses an engine.
    If it does, it deletes the content of the database, so the test has a fresh db to work with.
    """

    for engine_name in ("engine", "engine_with_test_resource"):
        if engine_name in request.fixturenames:
            engine = request.getfixturevalue(engine_name)
            with engine.connect() as connection:
                transaction = connection.begin()
                if engine_name == "engine":
                    for table in Base.metadata.tables.values():
                        connection.execute(table.delete())
                elif engine_name == "engine_with_test_resource":
                    for table in OrmTestResource.metadata.tables.values():
                        connection.execute(table.delete())
                    stmt = insert(OrmTestResource).values(
                        title="A title", platform="example", platform_identifier="1"
                    )
                    connection.execute(stmt)
                transaction.commit()


@pytest.fixture(scope="session")
def client(engine: Engine) -> TestClient:
    """
    Create a TestClient that can be used to mock sending requests to our application
    """
    app = FastAPI()
    add_routes(app, engine)
    return TestClient(app)


@pytest.fixture(scope="session")
def client_test_resource(engine_with_test_resource: Engine) -> TestClient:
    """A Startlette TestClient including routes to the TestResource, only in "aiod" schema"""
    app = FastAPI()
    app.include_router(RouterTestResource().create(engine_with_test_resource, ""))
    return TestClient(app)
