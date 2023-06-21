from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey


class ComputationalResourceEndpoint(SQLModel):
    endpoint: str | None = Field(
        max_length=250,
        schema_extra={"example": "uri examplexs"},
    )
    name: str | None = Field(max_length=150, schema_extra={"example": "Name of this file."})


class ComputationalResourceEndpointOrm(ComputationalResourceEndpoint, table=True):  # type: ignore [call-arg]  # noqa E501
    __tablename__ = "computational_resource_endpoint"
    identifier: int | None = Field(primary_key=True)

    computational_resource_identifier: int | None = Field(
        sa_column=Column(
            Integer, ForeignKey("computational_resource.identifier", ondelete="CASCADE")
        )
    )
