# from typing import Type
#
# from converters import organisation_converter_instance
# from converters.orm_converters.orm_converter import OrmConverter
# from database.model.organisation import OrmOrganisation
# from routers import ResourceRouter
# from schemas import AIoDOrganisation
#
#
# class OrganisationRouter(ResourceRouter[OrmOrganisation, AIoDOrganisation]):
#     @property
#     def version(self) -> int:
#         return 0
#
#     @property
#     def resource_name(self) -> str:
#         return "organisation"
#
#     @property
#     def resource_name_plural(self) -> str:
#         return "organisations"
#
#     @property
#     def aiod_class(self) -> Type[AIoDOrganisation]:
#         return AIoDOrganisation
#
#     @property
#     def orm_class(self) -> Type[OrmOrganisation]:
#         return OrmOrganisation
#
#     @property
#     def converter(self) -> OrmConverter[AIoDOrganisation, OrmOrganisation]:
#         return organisation_converter_instance
