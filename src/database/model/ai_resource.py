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
    def create_or_get(cls, session: Session, *arg, create: bool = True, **kw):
        """
        If create=True, create a new Orm object. If False, try to get an existing instance from
        the database, or create a new instance if that failed.
        """
        if len(arg) > 0:
            raise ValueError("Please use only keyword arguments, to avoid mistakes")
        if create:
            return cls(**kw)
        return cls.as_unique(session, **kw)
