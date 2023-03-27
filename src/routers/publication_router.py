from typing import Type

from converters import publication_converter
from database.model.publication import OrmPublication
from routers.abstract_router import ResourceRouter, AIOD_CLASS, ORM_CLASS
from schemas import AIoDPublication


class PublicationRouter(ResourceRouter[OrmPublication, AIoDPublication]):
    @property
    def resource_name(self) -> str:
        return "publication"

    @property
    def resource_name_plural(self) -> str:
        return "publications"

    @property
    def aiod_class(self) -> Type[AIOD_CLASS]:
        return AIoDPublication

    @property
    def orm_class(self) -> Type[ORM_CLASS]:
        return OrmPublication

    @property
    def converter(self):
        return publication_converter
