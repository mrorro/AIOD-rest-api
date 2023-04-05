import abc
from typing import Generic, TypeVar, Type

from schemas import AIoDResource

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDResource)
SCHEMA_CLASS = TypeVar("SCHEMA_CLASS")


class SchemaConverter(abc.ABC, Generic[AIOD_CLASS, SCHEMA_CLASS]):
    @property
    @abc.abstractmethod
    def schema_documentation(self) -> str:
        """
        Information regarding the schema to be used in the swagger documentation
        """

    @property
    @abc.abstractmethod
    def to_class(self) -> Type[SCHEMA_CLASS]:
        pass

    @abc.abstractmethod
    def convert(self, aiod: AIOD_CLASS) -> SCHEMA_CLASS:
        pass
