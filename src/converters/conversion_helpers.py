from typing import TypeVar, Set, Type, List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.model.base import Base

T = TypeVar("T", bound=Base)


def retrieve_related_objects_by_ids(session: Session, ids: Set[int], cls: Type[T]) -> List[T]:
    related_objects = []
    if len(ids) > 0:
        query = select(cls).where(cls.identifier.in_(ids))
        related_objects = session.scalars(query).all()
        if len(related_objects) != len(ids):
            ids_not_found = sorted(set(ids) - {c.identifier for c in related_objects})
            ids_not_found_str = ", ".join(str(id_) for id_ in ids_not_found)
            raise HTTPException(
                status_code=404,
                detail=f"Related {cls.__name__}'s with identifiers {ids_not_found_str} not found "
                f"in the database.",
            )
    return related_objects
