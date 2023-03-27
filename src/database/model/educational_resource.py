from sqlite3 import Date
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Table, Column, String, DateTime, Boolean, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.model.base import Base

educational_resource_business_category_relationship = Table(
    "educational_resource_business_category",
    Base.metadata,
    Column(
        "educational_resource_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "business_category_id",
        ForeignKey("business_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

educational_resource_technical_category_relationship = Table(
    "educational_resource_technical_category",
    Base.metadata,
    Column(
        "educational_resource_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "technical_category_id",
        ForeignKey("technical_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

educational_resource_tag_relationship = Table(
    "educational_resource_tag",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "tag_id", ForeignKey("tags.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True
    ),
)


educational_resource_target_audience_relationship = Table(
    "educational_resource_target_audience",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "target_audience_id",
        ForeignKey("target_audience.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
)


educational_resource_language_relationship = Table(
    "educational_resource_language",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "language_id",
        ForeignKey("languages.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
)


class EducationalResource(Base):
    """Any educational resource"""

    __tablename__ = "educational_resources"

    # required fields
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    date_modified: Mapped[Date] = mapped_column(DateTime(timezone=True), server_default=func.now())
    body: Mapped[str] = mapped_column(String(500), nullable=False)
    website_url: Mapped[str] = mapped_column(String(500), nullable=False)
    educational_role: Mapped[str] = mapped_column(String(500), nullable=False)
    educational_level: Mapped[str] = mapped_column(String(500), nullable=False)
    educatonal_type: Mapped[str] = mapped_column(String(500), nullable=False)
    pace: Mapped[str] = mapped_column(String(500), nullable=False)

    # optional fields
    interactivity_type: Mapped[str] = mapped_column(String(500), nullable=True)
    accessibility_api: Mapped[str] = mapped_column(String(500), nullable=True)
    accessibility_control: Mapped[str] = mapped_column(String(500), nullable=True)
    access_mode: Mapped[str] = mapped_column(String(500), nullable=True)
    access_restrictions: Mapped[str] = mapped_column(String(500), nullable=True)
    citation: Mapped[str] = mapped_column(String(500), nullable=True)
    version: Mapped[str] = mapped_column(String(500), nullable=True)
    field_prerequisites: Mapped[str] = mapped_column(String(500), nullable=True)
    short_summary: Mapped[str] = mapped_column(String(500), nullable=True)

    duration_minutes_and_hours: Mapped[str] = mapped_column(String(500), nullable=True)
    hours_per_week: Mapped[str] = mapped_column(String(500), nullable=True)
    country: Mapped[str] = mapped_column(String(500), nullable=True)

    is_accessible_for_free: Mapped[Boolean] = mapped_column(Boolean, nullable=True)
    duration_in_years: Mapped[int] = mapped_column(nullable=True)

    time_required: Mapped[Interval] = mapped_column(Interval, nullable=True)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    # relationships

    business_categories = relationship(
        "BusinessCategory",
        secondary=educational_resource_business_category_relationship,
        backref="educational_resource_business_categories",
        passive_deletes=True,
    )

    technical_categories = relationship(
        "TechnicalCategory",
        secondary=educational_resource_technical_category_relationship,
        backref="educational_resource_technical_categories",
        passive_deletes=True,
    )

    tags = relationship(
        "Tag",
        secondary=educational_resource_tag_relationship,
        backref="educational_resource_tags",
        passive_deletes=True,
    )

    target_audience = relationship(
        "TargetAudience",
        secondary=educational_resource_target_audience_relationship,
        backref="educational_resource_target_audience",
        passive_deletes=True,
    )

    languages = relationship(
        "Language",
        secondary=educational_resource_language_relationship,
        backref="educational_resource_languages",
        passive_deletes=True,
    )
