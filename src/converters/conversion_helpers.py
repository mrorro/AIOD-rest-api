from typing import TypeVar, Set, Type, List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.model.base import Base

T = TypeVar("T", bound=Base)


def retrieve_related_objects_by_ids(session: Session, ids: Set[str], cls: Type[T]) -> List[T]:
    related_objects = []
    if len(ids) > 0:
        query = select(cls).where(cls.id.in_(ids))
        related_objects = session.scalars(query).all()
        if len(related_objects) != len(ids):
            ids_not_found = set(ids) - {c.id for c in related_objects}
            raise HTTPException(
                status_code=404,
                detail=f"Dataset parts '{', '.join(ids_not_found)}' not found in the database.",
            )
    return related_objects
