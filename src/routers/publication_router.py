from typing import Type

from converters import publication_converter_instance
from converters.orm_converters.abstract_converter import OrmConverter
from database.model.publication import OrmPublication
from routers.abstract_router import ResourceRouter
from schemas import AIoDPublication


class PublicationRouter(ResourceRouter[OrmPublication, AIoDPublication]):
    @property
    def resource_name(self) -> str:
        return "publication"

    @property
    def resource_name_plural(self) -> str:
        return "publications"

    @property
    def aiod_class(self) -> Type[AIoDPublication]:
        return AIoDPublication

    @property
    def orm_class(self) -> Type[OrmPublication]:
        return OrmPublication

    @property
    def converter(self) -> OrmConverter[AIoDPublication, OrmPublication]:
        return publication_converter_instance
