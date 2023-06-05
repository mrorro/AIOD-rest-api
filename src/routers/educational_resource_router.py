# from typing import Type
#
# from converters import educational_resource_converter_instance
# from converters.orm_converters.orm_converter import OrmConverter
# from database.model.educational_resource import OrmEducationalResource
# from routers.resource_router import ResourceRouter
# from schemas import AIoDEducationalResource
#
from database.model.educational_resource import EducationalResource
from routers.resource_router import ResourceRouter


class EducationalResourceRouter(ResourceRouter):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "educational_resource"

    @property
    def resource_name_plural(self) -> str:
        return "educational_resources"

    @property
    def resource_class(self) -> type[EducationalResource]:
        return EducationalResource
