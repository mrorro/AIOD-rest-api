from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey


class ComputationalResourceEndpoint(SQLModel):
    name: str | None = Field(max_length=150, schema_extra={"example": "www.example.com/endpoint"})


class ComputationalResourceEndpointOrm(ComputationalResourceEndpoint, table=True):  # type: ignore [call-arg]  # noqa E501
    __tablename__ = "computational_resource_endpoint"
    identifier: int | None = Field(primary_key=True)

    computational_resource_identifier: int | None = Field(
        sa_column=Column(
            Integer, ForeignKey("computational_resource.identifier", ondelete="CASCADE")
        )
    )
