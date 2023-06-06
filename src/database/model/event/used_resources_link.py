from sqlmodel import SQLModel, Field


class EventUsedResourcesLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_used_resources_link"
    event_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    used_resources_identifier: int = Field(foreign_key="ai_asset.identifier", primary_key=True)
