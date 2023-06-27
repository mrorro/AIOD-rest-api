from typing import Type
from database.model.news.news import News
from routers.resource_router import ResourceRouter


class NewsRouter(ResourceRouter):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "news"

    @property
    def resource_name_plural(self) -> str:
        return "news"

    @property
    def resource_class(self) -> Type[News]:
        return News
