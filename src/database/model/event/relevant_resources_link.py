from sqlmodel import SQLModel, Field


class EventRelevantResourcesLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_relevant_resources_link"
    event_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    relevant_resources_identifier: int = Field(
        foreign_key="ai_asset_table.identifier", primary_key=True
    )
