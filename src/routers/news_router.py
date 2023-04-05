from typing import Type

from converters import news_converter_instance
from converters.orm_converters.abstract_converter import OrmConverter
from database.model.news import OrmNews
from routers.abstract_router import ResourceRouter
from schemas import AIoDNews


class NewsRouter(ResourceRouter[OrmNews, AIoDNews]):
    @property
    def resource_name(self) -> str:
        return "news"

    @property
    def resource_name_plural(self) -> str:
        return "news"

    @property
    def aiod_class(self) -> Type[AIoDNews]:
        return AIoDNews

    @property
    def orm_class(self) -> Type[OrmNews]:
        return OrmNews

    @property
    def converter(self) -> OrmConverter[AIoDNews, OrmNews]:
        return news_converter_instance
