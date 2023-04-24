import tempfile
from typing import Type, Any
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from pydantic import Field, BaseModel
from sqlalchemy import String, create_engine, Engine
from sqlalchemy.orm import Mapped, mapped_column, Session
from starlette.testclient import TestClient

from converters import OrmConverter
from converters.schema_converters.schema_converter import SchemaConverter
from database.model.resource import OrmResource
from routers import ResourceRouter
from schemas import AIoDResource


class OrmTestResource(OrmResource):
    """Resource only used for unittests"""

    __tablename__ = "test_resource"
    title: Mapped[str] = mapped_column(String(250), nullable=False)


class AIoDTestResource(AIoDResource):
    """Resource only used for unittests"""

    title: str = Field(max_length=250)


class SchemaClass(BaseModel):
    """Alternative schema for the AIoDTestResource, only used for unittests"""

    title_with_alternative_name: str = Field(max_length=250)


class SchemaConverterTestResource(SchemaConverter[AIoDTestResource, SchemaClass]):
    """Converting the AIoDTestResource into SchemaClass, only used for unittests"""

    @property
    def to_class(self) -> Type[SchemaClass]:
        return SchemaClass

    def convert(self, aiod: AIoDTestResource) -> SchemaClass:
        return SchemaClass(title_with_alternative_name=aiod.title)


converter = Mock(spec=OrmConverter)
converter.orm_to_aiod = Mock(
    return_value=AIoDTestResource(title="A title", platform="example", platform_identifier=1)
)


class RouterAIoDOnly(ResourceRouter[OrmTestResource, AIoDTestResource]):
    """Router with only "aiod" as possible output format, used only for unittests"""

    @property
    def resource_name(self) -> str:
        return "test_resource"

    @property
    def resource_name_plural(self) -> str:
        return "test_resources"

    @property
    def aiod_class(self) -> Type[AIoDTestResource]:
        return AIoDTestResource

    @property
    def orm_class(self) -> Type[OrmTestResource]:
        return OrmTestResource

    @property
    def converter(self) -> OrmConverter[AIoDTestResource, OrmTestResource]:
        return converter


class RouterWithOtherSchema(RouterAIoDOnly):
    """Router with "aiod" and "other-schema" as possible output format, used only for unittests"""

    @property
    def schema_converters(self) -> dict[str, SchemaConverter[AIoDTestResource, Any]]:
        return {"other-schema": SchemaConverterTestResource()}


@pytest.fixture(scope="module")
def engine_with_test_resource() -> Engine:
    """Create a SqlAlchemy Engine populated with an instance of the TestResource"""
    temporary_file = tempfile.NamedTemporaryFile()
    engine = create_engine(f"sqlite:///{temporary_file.name}")
    OrmTestResource.metadata.create_all(engine)
    test_instance = OrmTestResource(title="A title", platform="example", platform_identifier="1")
    with Session(engine) as session:
        session.add(test_instance)
        session.commit()
    return engine


@pytest.fixture(scope="module")
def client_aiod_only(engine_with_test_resource) -> TestClient:
    """A Startlette TestClient including routes to the TestResource, only in "aiod" schema"""
    app = FastAPI()
    app.include_router(RouterAIoDOnly().create(engine_with_test_resource, ""))
    return TestClient(app)


@pytest.fixture(scope="module")
def client_with_other_schema(engine_with_test_resource) -> TestClient:
    """A Startlette TestClient including routes to the TestResource, using schemas "aiod" and
    "other-schema" """
    app = FastAPI()
    app.include_router(RouterWithOtherSchema().create(engine_with_test_resource, ""))
    return TestClient(app)


@pytest.mark.parametrize("schema_string", ["", "?schema=aiod"])
def test_resources_aiod(
    client_aiod_only: TestClient,
    client_with_other_schema: TestClient,
    schema_string: str,
):
    for client in [client_with_other_schema, client_aiod_only]:
        response = client.get("/test_resources" + schema_string)
        assert response.status_code == 200
        json_ = response.json()
        assert len(json_) == 1
        assert json_[0]["title"] == "A title"
        assert "title_with_alternative_name" not in json_[0]


@pytest.mark.parametrize("schema_string", ["", "?schema=aiod"])
def test_resource_aiod(
    client_aiod_only: TestClient,
    client_with_other_schema: TestClient,
    schema_string: str,
):
    for client in [client_with_other_schema, client_aiod_only]:
        response = client.get("/test_resources/1" + schema_string)
        assert response.status_code == 200
        json_ = response.json()
        assert json_["title"] == "A title"
        assert "title_with_alternative_name" not in json_


@pytest.mark.parametrize("url_part", ["?schema=other-schema", "/1?schema=other-schema"])
def test_aiod_only_other_schema(client_aiod_only: TestClient, url_part: str):
    response = client_aiod_only.get("/test_resources" + url_part)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "unexpected value; permitted: 'aiod'"


def test_resources_other_schema(client_with_other_schema: TestClient):
    response = client_with_other_schema.get("/test_resources?schema=other-schema")
    assert response.status_code == 200
    json_ = response.json()
    assert len(json_) == 1
    assert json_[0]["title_with_alternative_name"] == "A title"
    assert "title" not in json_[0]


def test_resource_other_schema(client_with_other_schema: TestClient):
    response = client_with_other_schema.get("/test_resources/1?schema=other-schema")
    assert response.status_code == 200
    json_ = response.json()
    assert json_["title_with_alternative_name"] == "A title"
    assert "title" not in json_


@pytest.mark.parametrize(
    "url", ["/test_resources?schema=nonexistent", "/test_resources/1?schema=nonexistent"]
)
def test_nonexistent_schema(client_with_other_schema: TestClient, url: str):
    response = client_with_other_schema.get(url)
    assert response.status_code == 422
    msg = response.json()["detail"][0]["msg"]
    assert msg == "unexpected value; permitted: 'aiod', 'other-schema'"
