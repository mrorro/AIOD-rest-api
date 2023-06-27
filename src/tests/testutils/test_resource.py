"""
Test resource with router and mocked converter
"""

from typing import Type

from sqlmodel import Field

from database.model.resource import Resource
from routers import ResourceRouter


class TestResourceBase(Resource):
    title: str = Field(max_length=250, nullable=False, unique=True)


class TestResource(TestResourceBase, table=True):  # type: ignore [call-arg]
    identifier: int = Field(default=None, primary_key=True)


class RouterTestResource(ResourceRouter):
    """Router with only "aiod" as possible output format, used only for unittests"""

    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "test_resource"

    @property
    def resource_name_plural(self) -> str:
        return "test_resources"

    @property
    def resource_class(self) -> Type[TestResource]:
        return TestResource
