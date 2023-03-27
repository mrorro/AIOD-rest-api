"""
Contains the definitions for the different tables in our database.
See also:
   * https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column # noqa
   * https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses

Note: because we use MySQL in the demo, we need to explicitly set maximum string lengths.
"""
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.model.base import Base
from database.model.dataset_relationships import (
    dataset_keyword_relationship,
    dataset_license_relationship,
)
from database.model.news_relationships import news_tag_relationship
from database.model.unique_model import UniqueMixin

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset import OrmDataset
    from database.model.news import OrmNews


class OrmLicense(UniqueMixin, Base):
    """
    A license document, indicated by URL.

    For now only related to datasets, but we can extend it with relationships to other resources.
    """

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "licenses"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    datasets: Mapped[list["OrmDataset"]] = relationship(
        default_factory=list,
        back_populates="license",
        secondary=dataset_license_relationship,
    )


class OrmKeyword(UniqueMixin, Base):
    """
    Keywords or tags used to describe some item

    For now only related to datasets and news, but we can extend it with relationships to other
    resources.
    """

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "keywords"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    datasets: Mapped[list["OrmDataset"]] = relationship(
        default_factory=list,
        back_populates="keywords",
        secondary=dataset_keyword_relationship,
    )
    news: Mapped[list["OrmNews"]] = relationship(
        default_factory=list,
        back_populates="tags",
        secondary=news_tag_relationship,
    )
