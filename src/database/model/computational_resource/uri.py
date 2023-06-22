from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey


class ComputationalResourceUri(SQLModel):
    uri: str | None = Field(
        max_length=250,
        schema_extra={"example": "uri examples"},
    )
    name: str | None = Field(max_length=150, schema_extra={"example": "https://www.example.com"})


class ComputationalResourceUriOrm(ComputationalResourceUri, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_uri"
    identifier: int | None = Field(primary_key=True)

    computational_resource_identifier: int | None = Field(
        sa_column=Column(
            Integer, ForeignKey("computational_resource.identifier", ondelete="CASCADE")
        )
    )
