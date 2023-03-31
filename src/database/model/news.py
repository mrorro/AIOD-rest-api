from sqlite3 import Date

from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.model.base import Base
from database.model.general import OrmKeyword, OrmBusinessCategory
from database.model.news_relationships import (
    news_business_category_relationship,
    news_news_category_relationship,
    news_keyword_relationship,
    news_media_relationship,
)
from database.model.resource import OrmResource
from database.model.unique_model import UniqueMixin


class OrmMedia(UniqueMixin, Base):
    """Any media"""

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "media"

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)
    news: Mapped[list["OrmNews"]] = relationship(
        default_factory=list,
        back_populates="media",
        secondary=news_media_relationship,
    )


class OrmNewsCategory(UniqueMixin, Base):
    """Any news category"""

    @classmethod
    def _unique_hash(cls, category, **_):
        return category

    @classmethod
    def _unique_filter(cls, query, category, **_):
        return query.filter(cls.category == category)

    __tablename__ = "news_categories"

    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)
    category: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("news_categories.identifier"), nullable=True, default=None
    )
    parent_category = relationship("OrmNewsCategory")
    news: Mapped[list["OrmNews"]] = relationship(
        default_factory=list,
        back_populates="news_categories",
        secondary=news_news_category_relationship,
    )


class OrmNews(OrmResource):
    """Any news"""

    __tablename__ = "news"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    date_modified: Mapped[Date] = mapped_column(DateTime(timezone=True), server_default=func.now())
    body: Mapped[str] = mapped_column(String(2000), nullable=False)
    section: Mapped[str] = mapped_column(String(500), nullable=False)
    headline: Mapped[str] = mapped_column(String(500), nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(500), nullable=True)
    alternative_headline: Mapped[str] = mapped_column(String(500), nullable=True)

    business_categories: Mapped[list["OrmBusinessCategory"]] = relationship(
        secondary=news_business_category_relationship,
        back_populates="news",
        passive_deletes=True,
        default_factory=list,
    )
    news_categories: Mapped[list["OrmNewsCategory"]] = relationship(
        secondary=news_news_category_relationship,
        back_populates="news",
        passive_deletes=True,
        default_factory=list,
    )
    keywords: Mapped[list["OrmKeyword"]] = relationship(
        secondary=news_keyword_relationship,
        back_populates="news",
        passive_deletes=True,
        default_factory=list,
    )
    media: Mapped[list["OrmMedia"]] = relationship(
        secondary=news_media_relationship,
        back_populates="news",
        passive_deletes=True,
        default_factory=list,
    )
