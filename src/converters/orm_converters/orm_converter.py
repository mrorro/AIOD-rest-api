import abc
import datetime
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from database.model.resource import OrmResource
from schemas import AIoDResource

ORM_CLASS = TypeVar("ORM_CLASS", bound=OrmResource)
AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDResource)


class OrmConverter(abc.ABC, Generic[AIOD_CLASS, ORM_CLASS]):
    """
    Converting between resource representations.
    """

    @abc.abstractmethod
    def aiod_to_orm(
        self, session: Session, aiod: AIOD_CLASS, return_existing_if_present=False
    ) -> ORM_CLASS:
        """
        Convert an AIoD representation into the database representation and add it to the session.

            Parameters:
                session (Session): the SqlAlchemy session
                aiod (AIOD_CLASS): the AIoD instance
                return_existing_if_present (bool): if true, return existing object if it already
                    exists. If false, it will just return
        """
        pass

    @abc.abstractmethod
    def orm_to_aiod(self, orm: ORM_CLASS) -> AIOD_CLASS:
        """
        Convert a database representation into an AIoD representation
        """
        pass


def datetime_or_date(value: datetime.datetime | None) -> datetime.datetime | datetime.date | None:
    """
    Return None if the value is None, a date if the value does not has only a date and no time,
    otherwise return a datetime.
    """
    if value is None:
        return None
    if value.time() == datetime.time.min:
        return value.date()
    return value
