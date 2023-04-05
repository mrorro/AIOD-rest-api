from typing import Type

from converters import educational_resource_converter_instance
from converters.orm_converters.abstract_converter import OrmConverter
from database.model.educational_resource import OrmEducationalResource
from routers.abstract_router import ResourceRouter
from schemas import AIoDEducationalResource


class EducationalResourceRouter(ResourceRouter[OrmEducationalResource, AIoDEducationalResource]):
    @property
    def resource_name(self) -> str:
        return "educational_resources"

    @property
    def resource_name_plural(self) -> str:
        return "educational_resources"

    @property
    def aiod_class(self) -> Type[AIoDEducationalResource]:
        return AIoDEducationalResource

    @property
    def orm_class(self) -> Type[OrmEducationalResource]:
        return OrmEducationalResource

    @property
    def converter(self) -> OrmConverter[AIoDEducationalResource, OrmEducationalResource]:
        return educational_resource_converter_instance
