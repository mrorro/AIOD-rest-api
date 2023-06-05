from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import List
from database.model.event.research_area_link import EventResearchAreaLink
from database.model.general.research_areas import ResearchArea
from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource
from serialization import AttributeSerializer, FindByIdentifierDeserializer, FindByNameDeserializer


class EventParentChildLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_parent_child_link"
    parent_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    child_identifier: int = Field(foreign_key="event.identifier", primary_key=True)


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
    duration: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example duration Event"}
    )
    status: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example status Event"}
    )
    attendance_mode: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example attendance mode Event"}
    )
    type: str | None = Field(
        default=None, max_length=500, schema_extra={"example": "Example type Event"}
    )


class Event(EventBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "event"
    identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")
    # This entity is implemented in the pr 52, it atributes will be implemented after merging it
    # TODO add business_categories

    research_areas: List["ResearchArea"] = Relationship(
        back_populates="events", link_model=EventResearchAreaLink
    )
    sub_events: List["Event"] = Relationship(
        back_populates="super_events",
        link_model=EventParentChildLink,
        sa_relationship_kwargs=dict(
            primaryjoin="Event.identifier==EventParentChildLink.parent_identifier",
            secondaryjoin="Event.identifier==EventParentChildLink.child_identifier",
        ),
    )
    super_events: List["Event"] = Relationship(
        back_populates="sub_events",
        link_model=EventParentChildLink,
        sa_relationship_kwargs=dict(
            primaryjoin="Event.identifier==EventParentChildLink.child_identifier",
            secondaryjoin="Event.identifier==EventParentChildLink.parent_identifier",
        ),
    )

    class RelationshipConfig:
        sub_events: List[int] = ResourceRelationshipList(
            example=[3, 4],
            serializer=AttributeSerializer("identifier"),
        )
        super_events: List[int] = ResourceRelationshipList(
            example=[1, 2],
            serializer=AttributeSerializer("identifier"),
        )
        research_areas: List[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ResearchArea),
            example=["research_area1", "research_area2"],
        )


# Defined separate because it references Event, and can therefor not be defined inside Dataset
deserializer = FindByIdentifierDeserializer(Event)
Event.RelationshipConfig.super_events.deserializer = deserializer  # type: ignore[attr-defined]
Event.RelationshipConfig.sub_events.deserializer = deserializer  # type: ignore[attr-defined]
