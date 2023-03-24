from sqlite3 import Date
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Table, Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.model.base import Base

news_business_category_relationship = Table(
    "news_business_category",
    Base.metadata,
    Column("news_id", ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "business_category_id",
        ForeignKey("business_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

news_tag_relationship = Table(
    "news_tag",
    Base.metadata,
    Column(
        "news_id", ForeignKey("news.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True
    ),
    Column(
        "tag_id", ForeignKey("tags.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True
    ),
)

news_news_category_relationship = Table(
    "news_news_category",
    Base.metadata,
    Column("news_id", ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "news_category_id", ForeignKey("news_categories.id", ondelete="CASCADE"), primary_key=True
    ),
)

news_media_relationship = Table(
    "news_media",
    Base.metadata,
    Column("news_id", ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
)


class Media(Base):
    """Any media"""

    __tablename__ = "media"

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class NewsCategory(Base):
    """Any news category"""

    __tablename__ = "news_categories"

    category: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("news_categories.id"), nullable=True)
    parent_category = relationship("NewsCategory")
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class News(Base):
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

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    business_categories = relationship(
        "BusinessCategory",
        secondary=news_business_category_relationship,
        backref="business_categories",
        passive_deletes=True,
    )
    news_categories = relationship(
        "NewsCategory",
        secondary=news_news_category_relationship,
        backref="news_categories",
        passive_deletes=True,
    )
    tags = relationship(
        "Tag", secondary=news_tag_relationship, backref="news", passive_deletes=True
    )

    media = relationship(
        "Media", secondary=news_media_relationship, backref="news", passive_deletes=True
    )
