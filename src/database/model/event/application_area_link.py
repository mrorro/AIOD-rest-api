from sqlmodel import SQLModel, Field


class EventApplicationAreaLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_application_area_link"
    event_identifier: int = Field(foreign_key="event.identifier", primary_key=True)
    application_area_identifier: int = Field(
        foreign_key="application_area.identifier", primary_key=True
    )
