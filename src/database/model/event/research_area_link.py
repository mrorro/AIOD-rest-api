from sqlmodel import SQLModel, Field


class EventResearchAreaLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_research_area_link"
    educational_resource_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="research_area.identifier", primary_key=True)
