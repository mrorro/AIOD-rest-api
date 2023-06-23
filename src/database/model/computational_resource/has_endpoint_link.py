from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class ComputationalResourceHasEndpointLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_has_endpoint_link"
    computational_resource_identifier: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("computational_resource.identifier", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    endpoint_identifier: int = Field(
        foreign_key="computational_resource_endpoint.identifier", primary_key=True
    )
