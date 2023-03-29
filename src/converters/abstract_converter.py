import abc
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.model.base import Base

ORM_CLASS = TypeVar("ORM_CLASS", bound=Base)
AIOD_CLASS = TypeVar("AIOD_CLASS", bound=BaseModel)


class AbstractConverter(abc.ABC, Generic[AIOD_CLASS, ORM_CLASS]):
    """
    Converting between resource representations.
    """

    @abc.abstractmethod
    def aiod_to_orm(self, session: Session, orm: AIOD_CLASS) -> ORM_CLASS:
        """
        Convert an AIoD representation into the database representation
        """
        pass

    @abc.abstractmethod
    def orm_to_aiod(self, orm: ORM_CLASS) -> AIOD_CLASS:
        """
        Convert a database representation into an AIoD representation
        """
        pass
