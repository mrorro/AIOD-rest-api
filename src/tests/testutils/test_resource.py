"""
Test resource with router and mocked converter
"""

from typing import Type
from unittest.mock import Mock

from pydantic import Field
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from converters import OrmConverter
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


class RouterTestResource(ResourceRouter[OrmTestResource, AIoDTestResource]):
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
    def aiod_class(self) -> Type[AIoDTestResource]:
        return AIoDTestResource

    @property
    def orm_class(self) -> Type[OrmTestResource]:
        return OrmTestResource

    @property
    def converter(self) -> OrmConverter[AIoDTestResource, OrmTestResource]:
        converter = Mock(spec=OrmConverter)
        converter.orm_to_aiod = Mock(
            return_value=AIoDTestResource(
                title="A title", platform="example", platform_identifier=1
            )
        )
        converter.aiod_to_orm = Mock(
            return_value=OrmTestResource(title="test", platform="example", platform_identifier=1)
        )
        return converter
