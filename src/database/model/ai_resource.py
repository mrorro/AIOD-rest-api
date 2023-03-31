from sqlalchemy import String, and_
from sqlalchemy.orm import Mapped, mapped_column, Session

from database.model.base import Base
from database.model.unique_model import UniqueMixin


class OrmAIResource(UniqueMixin, Base):
    """
    The base class of all our AIResources such as Datasets, Publications, News etc..

    For now it only contains a couple of fields, we will have to extend it later.
    """

    __abstract__ = True

    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)
    platform: Mapped[str] = mapped_column(String(30), nullable=False)
    platform_identifier: Mapped[str | None] = mapped_column(String(250))

    @classmethod
    def _unique_hash(cls, platform: str = "", platform_identifier: str = "", **_):
        if platform == "" or platform_identifier == "":
            raise ValueError("")
        return f"platform:{platform}|id:{platform_identifier}"

    @classmethod
    def _unique_filter(
        cls, query, *args, platform: str = "", platform_identifier: str = "", **kwargs
    ):
        return query.filter(
            and_(cls.platform == platform, cls.platform_identifier == platform_identifier)
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
