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
    __tablename__ = "test_resource"
    title: Mapped[str] = mapped_column(String(250), nullable=False)


class AIoDTestResource(AIoDResource):
    title: str = Field(max_length=250)


class SchemaClass(BaseModel):
    title_with_alternative_name: str = Field(max_length=250)


converter = Mock(spec=OrmConverter)
converter.orm_to_aiod = Mock(
    return_value=AIoDTestResource(title="A title", platform="example", platform_identifier=1)
)


class SchemaConverterTestResource(SchemaConverter[AIoDTestResource, SchemaClass]):
    @property
    def to_class(self) -> Type[SchemaClass]:
        return SchemaClass

    def convert(self, aiod: AIoDTestResource) -> SchemaClass:
        return SchemaClass(title_with_alternative_name=aiod.title)


class RouterWithoutSchemaConverters(ResourceRouter[OrmTestResource, AIoDTestResource]):
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


class RouterWithSchemaConverters(RouterWithoutSchemaConverters):
    @property
    def schema_converters(self) -> dict[str, SchemaConverter[AIoDTestResource, Any]]:
        return {"other-schema": SchemaConverterTestResource()}


@pytest.fixture(scope="module")
def populated_test_engine() -> Engine:
    temporary_file = tempfile.NamedTemporaryFile()
    engine = create_engine(f"sqlite:///{temporary_file.name}")
    OrmTestResource.metadata.create_all(engine)
    test_instance = OrmTestResource(title="A title", platform="example", platform_identifier="1")
    with Session(engine) as session:
        session.add(test_instance)
        session.commit()
    return engine


@pytest.fixture(scope="module")
def client_without_schema_converters(populated_test_engine: Engine) -> TestClient:
    app = FastAPI()
    app.include_router(RouterWithoutSchemaConverters().create(populated_test_engine, ""))
    return TestClient(app)


@pytest.fixture(scope="module")
def client_with_schema_converters(populated_test_engine: Engine) -> TestClient:
    app = FastAPI()
    app.include_router(RouterWithSchemaConverters().create(populated_test_engine, ""))
    return TestClient(app)


@pytest.mark.parametrize("schema_string", ["", "?schema=aiod"])
def test_resources_aiod(
    client_without_schema_converters: TestClient,
    client_with_schema_converters: TestClient,
    schema_string: str,
):
    for client in [client_with_schema_converters, client_without_schema_converters]:
        response = client.get("/test_resources" + schema_string)
        assert response.status_code == 200
        json_ = response.json()
        assert len(json_) == 1
        assert json_[0]["title"] == "A title"
        assert "title_with_alternative_name" not in json_[0]


@pytest.mark.parametrize("schema_string", ["", "?schema=aiod"])
def test_resource_aiod(
    client_without_schema_converters: TestClient,
    client_with_schema_converters: TestClient,
    schema_string: str,
):
    for client in [client_with_schema_converters, client_without_schema_converters]:
        response = client.get("/test_resources/1" + schema_string)
        assert response.status_code == 200
        json_ = response.json()
        assert json_["title"] == "A title"
        assert "title_with_alternative_name" not in json_


@pytest.mark.parametrize("url_part", ["?schema=other-schema", "/1?schema=other-schema"])
def test_without_schema_converters_other_schema(
    client_without_schema_converters: TestClient, url_part: str
):
    response = client_without_schema_converters.get("/test_resources" + url_part)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "unexpected value; permitted: 'aiod'"


def test_resources_with_schema_converters_other_schema(client_with_schema_converters: TestClient):
    response = client_with_schema_converters.get("/test_resources?schema=other-schema")
    assert response.status_code == 200
    json_ = response.json()
    assert len(json_) == 1
    assert json_[0]["title_with_alternative_name"] == "A title"
    assert "title" not in json_[0]


def test_resource_with_schema_converters_other_schema(client_with_schema_converters: TestClient):
    response = client_with_schema_converters.get("/test_resources/1?schema=other-schema")
    assert response.status_code == 200
    json_ = response.json()
    assert json_["title_with_alternative_name"] == "A title"
    assert "title" not in json_


@pytest.mark.parametrize(
    "url", ["/test_resources?schema=unexisting", "/test_resources/1?schema=unexisting"]
)
def test_with_schema_converters_unexisting_schema(
    client_with_schema_converters: TestClient, url: str
):
    response = client_with_schema_converters.get(url)
    assert response.status_code == 422
    msg = response.json()["detail"][0]["msg"]
    assert msg == "unexpected value; permitted: 'aiod', 'other-schema'"
