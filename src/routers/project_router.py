from typing import Type

from converters import project_converter_instance, OrmConverter
from database.model.project import OrmProject
from routers.resource_router import ResourceRouter
from schemas import AIoDProject


class ProjectRouter(ResourceRouter[OrmProject, AIoDProject]):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "project"

    @property
    def resource_name_plural(self) -> str:
        return "projects"

    @property
    def aiod_class(self) -> Type[AIoDProject]:
        return AIoDProject

    @property
    def orm_class(self) -> Type[OrmProject]:
        return OrmProject

    @property
    def converter(self) -> OrmConverter[AIoDProject, OrmProject]:
        return project_converter_instance
