from typing import Type

from converters import event_converter_instance, OrmConverter
from database.model.event import OrmEvent
from routers.resource_router import ResourceRouter
from schemas import AIoDEvent


class EventRouter(ResourceRouter[OrmEvent, AIoDEvent]):
    @property
    def resource_name(self) -> str:
        return "event"

    @property
    def resource_name_plural(self) -> str:
        return "events"

    @property
    def aiod_class(self) -> Type[AIoDEvent]:
        return AIoDEvent

    @property
    def orm_class(self) -> Type[OrmEvent]:
        return OrmEvent

    @property
    def converter(self) -> OrmConverter[AIoDEvent, OrmEvent]:
        return event_converter_instance
