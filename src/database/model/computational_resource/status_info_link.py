from sqlmodel import SQLModel, Field


class ComputationalResourceStatusInfoLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_status_info_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    uri_identifier: int = Field(
        foreign_key="computational_resource_uri.identifier", primary_key=True
    )
