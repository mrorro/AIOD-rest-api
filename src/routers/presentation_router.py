# from typing import Type
#
# from converters import presentation_converter_instance
# from converters.orm_converters.orm_converter import OrmConverter
# from database.model.presentation import OrmPresentation
# from database.model.publication import OrmPublication
# from routers.resource_router import ResourceRouter
# from schemas import AIoDPresentation
#
#
# class PresentationRouter(ResourceRouter[OrmPresentation, AIoDPresentation]):
#     @property
#     def version(self) -> int:
#         return 0
#
#     @property
#     def resource_name(self) -> str:
#         return "presentation"
#
#     @property
#     def resource_name_plural(self) -> str:
#         return "presentations"
#
#     @property
#     def aiod_class(self) -> Type[AIoDPresentation]:
#         return AIoDPresentation
#
#     @property
#     def orm_class(self) -> Type[OrmPresentation]:
#         return OrmPresentation
#
#     @property
#     def converter(self) -> OrmConverter[AIoDPresentation, OrmPublication]:
#         return presentation_converter_instance
