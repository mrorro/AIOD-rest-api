from typing import Type

from converters import organization_converter_instance
from converters.abstract_converter import ResourceConverter
from database.model.organization import OrmOrganization
from routers.abstract_router import ResourceRouter, AIOD_CLASS, ORM_CLASS
from schemas import AIoDOrganization


class OrganizationRouter(ResourceRouter[OrmOrganization, AIoDOrganization]):
    @property
    def resource_name(self) -> str:
        return "organization"

    @property
    def resource_name_plural(self) -> str:
        return "organizations"

    @property
    def aiod_class(self) -> Type[AIOD_CLASS]:
        return AIoDOrganization

    @property
    def orm_class(self) -> Type[ORM_CLASS]:
        return OrmOrganization

    @property
    def converter(self) -> ResourceConverter[AIOD_CLASS, ORM_CLASS]:
        return organization_converter_instance
