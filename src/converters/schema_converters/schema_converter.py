import abc
from typing import Generic, TypeVar, Type

from schemas import AIoDResource

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDResource)
SCHEMA_CLASS = TypeVar("SCHEMA_CLASS")


class SchemaConverter(abc.ABC, Generic[AIOD_CLASS, SCHEMA_CLASS]):
    """Converting between our AIoD representation of a resource and another representation. For
    example, for dataset, we can convert it to schema.org or DCAT-AP formats.

    This makes it easier for other services to connect to AIoD. Instead of adapting to the AIoD
    schema, they can use existing standards.
    """

    @property
    @abc.abstractmethod
    def to_class(self) -> Type[SCHEMA_CLASS]:
        pass

    @abc.abstractmethod
    def convert(self, aiod: AIOD_CLASS) -> SCHEMA_CLASS:
        pass
