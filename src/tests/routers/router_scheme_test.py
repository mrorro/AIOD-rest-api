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


def test_router_without_schema_converters(populated_test_engine: Engine):
    app = FastAPI()
    app.include_router(RouterWithoutSchemaConverters().create(populated_test_engine, ""))
    client = TestClient(app)
    for url in ["/test_resources", "/test_resources?schema=aiod"]:
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
    response = client.get("/test_resources?schema=other-schema")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "unexpected value; permitted: 'aiod'"


def test_router_with_schema_converters(populated_test_engine: Engine):
    app = FastAPI()
    app.include_router(RouterWithSchemaConverters().create(populated_test_engine, ""))
    client = TestClient(app)
    for url in ["/test_resources", "/test_resources?schema=aiod"]:
        response = client.get(url)
        assert response.status_code == 200
        json_ = response.json()
        assert len(json_) == 1
        assert json_[0]["title"] == "A title"
        assert "title_with_alternative_name" not in json_[0]
    response = client.get("/test_resources?schema=other-schema")
    assert response.status_code == 200
    json_ = response.json()
    assert len(json_) == 1
    assert json_[0]["title_with_alternative_name"] == "A title"
    assert "title" not in json_[0]

    response = client.get("/test_resources?schema=nonexistent-schema")
    assert response.status_code == 422
    error_msg = response.json()["detail"][0]["msg"]
    assert error_msg == "unexpected value; permitted: 'aiod', 'other-schema'"
