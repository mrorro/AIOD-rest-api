from datetime import datetime
from sqlmodel import Field
from database.model.resource import Resource


class EventBase(Resource):
    # Required fields
    name: str = Field(max_length=500, schema_extra={"example": "Example Event"})
    description: str = Field(max_length=5000, schema_extra={"example": "example descriprion"})
    registration_url: str = Field(
        max_length=500, schema_extra={"example": "https://example.com/event/example/registration"}
    )
    location: str = Field(max_length=500, schema_extra={"example": "Example location Event"})
    # Recommended fields
    start_date: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00"}
    )
    end_date: datetime | None = Field(default=None, schema_extra={"example": "2022-01-01T15:15:00"})
    duration: str = Field(max_length=500, schema_extra={"example": "Example duration Event"})
    status: str = Field(max_length=500, schema_extra={"example": "Example status Event"})
    attendance_mode: str = Field(
        max_length=500, schema_extra={"example": "Example attendance mode Event"}
    )
    type: str = Field(max_length=500, schema_extra={"example": "Example type Event"})


class Event(EventBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "event"
    identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")
