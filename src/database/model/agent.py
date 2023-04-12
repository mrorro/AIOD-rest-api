from sqlalchemy import String, ForeignKey, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.declarative import declared_attr

from database.model.base import Base
from database.model.unique_model import UniqueMixin


class OrmEmail(UniqueMixin, Base):
    __tablename__ = "emails"

    @classmethod
    def _unique_hash(cls, email):
        return email

    @classmethod
    def _unique_filter(cls, query, email):
        return query.filter(cls.email == email)

    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)

    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.identifier", ondelete="cascade"), nullable=True, default=None
    )


class OrmAgent(UniqueMixin, Base):
    """The class of agents"""

    __abstract__ = True

    # required fields
    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    # optional fields
    image_url: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # relationships
    @declared_attr
    def _email_addresses(cls):
        return relationship(OrmEmail)

    @classmethod
    def _unique_filter(cls, query, *args, name: str = "", **kwargs):
        return query.filter(and_(cls.name == name))

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
