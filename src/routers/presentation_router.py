from database.model.presentation.presentation import Presentation
from routers.resource_router import ResourceRouter


class PresentationRouter(ResourceRouter):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "presentation"

    @property
    def resource_name_plural(self) -> str:
        return "presentations"

    @property
    def resource_class(self) -> type[Presentation]:
        return Presentation
