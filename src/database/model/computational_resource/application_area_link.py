from sqlmodel import SQLModel, Field


class ComputationalResourceApplicationAreaLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_application_area_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    application_area_identifier: int = Field(
        foreign_key="application_area.identifier", primary_key=True
    )
