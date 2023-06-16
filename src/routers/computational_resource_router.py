from database.model.computational_resource.computational_resource import ComputationalResource
from routers.resource_router import ResourceRouter


class ComputationalResourceRouter(ResourceRouter):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "computational_resource"

    @property
    def resource_name_plural(self) -> str:
        return "computational_resources"

    @property
    def resource_class(self) -> type[ComputationalResource]:
        return ComputationalResource
