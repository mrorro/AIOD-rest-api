from sqlmodel import SQLModel, Field


class ComputationalResourceUri(SQLModel):
    name: str | None = Field(max_length=150, schema_extra={"example": "https://www.example.com"})


class ComputationalResourceUriOrm(ComputationalResourceUri, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_uri"
    identifier: int | None = Field(primary_key=True)
