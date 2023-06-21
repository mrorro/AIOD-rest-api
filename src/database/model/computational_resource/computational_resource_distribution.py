from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey


class ComputationalResourceDistributionBase(SQLModel):
    content_url: str = Field(
        max_length=250,
        schema_extra={"example": "https://www.example.com/computational_resource/file.csv"},
    )
    content_size_kb: int | None = Field(schema_extra={"example": 10000})
    description: str | None = Field(
        max_length=5000, schema_extra={"example": "Description of this file."}
    )
    encoding_format: str | None = Field(max_length=255, schema_extra={"example": "text/csv"})
    name: str | None = Field(max_length=150, schema_extra={"example": "Name of this file."})


class ComputationalResourceDistributionOrm(ComputationalResourceDistributionBase, table=True):  # type: ignore [call-arg]  # noqa E501
    __tablename__ = "computational_resource_distribution"
    identifier: int | None = Field(primary_key=True)

    computational_resource_identifier: int | None = Field(
        sa_column=Column(
            Integer, ForeignKey("computational_resource.identifier", ondelete="CASCADE")
        )
    )


class ComputationalResourceDistribution(ComputationalResourceDistributionBase):
    """All or part of a Dataset in downloadable form"""
