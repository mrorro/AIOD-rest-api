from datetime import datetime
from sqlmodel import Field
from database.model.resource import Resource


class EducationalResourceBase(Resource):
    # Required fields
    title: str = Field(max_length=150, schema_extra={"example": "Example News"})
    date_modified: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )
    body: str = Field(max_length=500, schema_extra={"example": "Example news body"})
    website_url: str = Field(
        max_length=500,
        schema_extra={"example": "https://example.com/educational_resource/example/website"},
    )
    educational_level: str = Field(
        max_length=500, schema_extra={"example": "Example educational level"}
    )
    educational_type: str = Field(
        max_length=500, schema_extra={"example": "Example educational type"}
    )
    pace: str = Field(max_length=500, schema_extra={"example": "Example pace"})
    # Recommended fields
    interactivity_type: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example interactivity type"}
    )
    typical_age_range: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example  typical age range"}
    )
    accessibility_api: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example accessibility api"}
    )
    accessibility_control: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example accessibility control"}
    )
    access_mode: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example access mode"}
    )
    access_mode_sufficient: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example access mode"}
    )
    access_restrictions: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example access restrictions"}
    )
    citations: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example citations"}
    )
    version: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example version"}
    )
    number_of_weeks: int | None = Field(default=None, schema_extra={"example": 0})
    field_prerequisites: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example field prerequisites"}
    )
    short_summary: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example short summary"}
    )
    duration_minutes_and_hours: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example duration minutes and hours"}
    )
    hours_per_week: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example hours per week"}
    )
    country: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example country"}
    )
    is_accessible_for_free: bool = Field(default=True, schema_extra={"example": True})
    credits: bool = Field(default=True, schema_extra={"example": True})
    duration_in_years: int | None = Field(default=None, schema_extra={"example": 0})


class EducationalResource(EducationalResourceBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "educational_resource"
    identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")
