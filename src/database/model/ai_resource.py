from sqlalchemy import String, and_
from sqlalchemy.orm import Mapped, mapped_column, Session

from database.model.base import Base
from database.model.unique_model import UniqueMixin


class OrmAIResource(UniqueMixin, Base):
    __abstract__ = True

    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)
    node: Mapped[str] = mapped_column(String(30), nullable=False)
    node_specific_identifier: Mapped[str | None] = mapped_column(String(250))

    @classmethod
    def _unique_hash(cls, node: str = "", node_specific_identifier: str = "", **_):
        if node == "" or node_specific_identifier == "":
            raise ValueError("")
        return f"Node:{node}|id:{node_specific_identifier}"

    @classmethod
    def _unique_filter(
        cls, query, *args, node: str = "", node_specific_identifier: str = "", **kwargs
    ):
        return query.filter(
            and_(cls.node == node, cls.node_specific_identifier == node_specific_identifier)
        )

    @classmethod
    def create(cls, session: Session, *arg, return_existing_if_present: bool = False, **kw):
        if return_existing_if_present:
            return cls.as_unique(session, *arg, **kw)
        return cls(*arg, **kw)
