import abc
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from database.model.ai_resource import OrmAIResource
from schemas import AIoDAIResource

ORM_CLASS = TypeVar("ORM_CLASS", bound=OrmAIResource)
AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDAIResource)


class ResourceConverter(abc.ABC, Generic[AIOD_CLASS, ORM_CLASS]):
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
