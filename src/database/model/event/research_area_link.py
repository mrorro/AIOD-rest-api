from sqlmodel import SQLModel, Field


class EventResearchAreaLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_research_area_link"
    event_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    research_area_identifier: int = Field(foreign_key="research_area.identifier", primary_key=True)
