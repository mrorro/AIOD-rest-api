from sqlite3 import Date
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, Boolean, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.ai_resource import OrmAIResource
from database.model.base import Base

from database.model.general import OrmBusinessCategory, OrmTechnicalCategory, OrmKeyword

from database.model.educational_resource_relationships import (
    educational_resource_business_category_relationship,
    educational_resource_technical_category_relationship,
    educational_resource_keyword_relationship,
    educational_resource_target_audience_relationship,
    educational_resource_language_relationship,
)
from database.model.unique_model import UniqueMixin


class OrmTargetAudience(UniqueMixin, Base):
    __tablename__ = "target_audience"

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    educational_resources: Mapped[list["OrmEducationalResource"]] = relationship(
        default_factory=list,
        back_populates="target_audience",
        secondary=educational_resource_target_audience_relationship,
    )


class OrmLanguage(UniqueMixin, Base):
    __tablename__ = "languages"

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    educational_resources: Mapped[list["OrmEducationalResource"]] = relationship(
        default_factory=list,
        back_populates="languages",
        secondary=educational_resource_language_relationship,
    )


class OrmEducationalResource(OrmAIResource):
    """Any educational resource"""

    __tablename__ = "educational_resources"

    # required fields
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    date_modified: Mapped[Date] = mapped_column(DateTime(timezone=True), server_default=func.now())
    body: Mapped[str] = mapped_column(String(500), nullable=False)
    website_url: Mapped[str] = mapped_column(String(500), nullable=False)
    educational_level: Mapped[str] = mapped_column(String(500), nullable=False)
    educational_type: Mapped[str] = mapped_column(String(500), nullable=False)
    pace: Mapped[str] = mapped_column(String(500), nullable=False)

    # optional fields
    interactivity_type: Mapped[str] = mapped_column(String(500), nullable=True)
    typical_age_range: Mapped[str] = mapped_column(String(500), nullable=True)
    accessibility_api: Mapped[str] = mapped_column(String(500), nullable=True)
    accessibility_control: Mapped[str] = mapped_column(String(500), nullable=True)
    access_mode: Mapped[str] = mapped_column(String(500), nullable=True)
    access_mode_sufficient: Mapped[str] = mapped_column(String(500), nullable=True)
    access_restrictions: Mapped[str] = mapped_column(String(500), nullable=True)
    citation: Mapped[str] = mapped_column(String(500), nullable=True)
    version: Mapped[str] = mapped_column(String(500), nullable=True)
    number_of_weeks: Mapped[int] = mapped_column(nullable=True)
    field_prerequisites: Mapped[str] = mapped_column(String(500), nullable=True)
    short_summary: Mapped[str] = mapped_column(String(500), nullable=True)

    duration_minutes_and_hours: Mapped[str] = mapped_column(String(500), nullable=True)
    hours_per_week: Mapped[str] = mapped_column(String(500), nullable=True)
    country: Mapped[str] = mapped_column(String(500), nullable=True)

    is_accessible_for_free: Mapped[Boolean] = mapped_column(Boolean, nullable=True)
    credits: Mapped[Boolean] = mapped_column(Boolean, nullable=True)
    duration_in_years: Mapped[int] = mapped_column(nullable=True)

    time_required: Mapped[Interval] = mapped_column(Interval, nullable=True)
    # relationships

    business_categories: Mapped[list["OrmBusinessCategory"]] = relationship(
        secondary=educational_resource_business_category_relationship,
        back_populates="educational_resources",
        passive_deletes=True,
        default_factory=list,
    )
    technical_categories: Mapped[list["OrmTechnicalCategory"]] = relationship(
        secondary=educational_resource_technical_category_relationship,
        back_populates="educational_resources",
        passive_deletes=True,
        default_factory=list,
    )
    keywords: Mapped[list["OrmKeyword"]] = relationship(
        secondary=educational_resource_keyword_relationship,
        back_populates="educational_resources",
        passive_deletes=True,
        default_factory=list,
    )
    target_audience: Mapped[list["OrmTargetAudience"]] = relationship(
        secondary=educational_resource_target_audience_relationship,
        back_populates="educational_resources",
        passive_deletes=True,
        default_factory=list,
    )
    languages: Mapped[list["OrmLanguage"]] = relationship(
        secondary=educational_resource_language_relationship,
        back_populates="educational_resources",
        passive_deletes=True,
        default_factory=list,
    )
