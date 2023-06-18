from typing import List
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

from database.model.dataset.checksum import ChecksumORM, Checksum
from database.model.relationships import ResourceRelationshipList
from serialization import CastDeserializer

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    pass


class DataDownloadBase(SQLModel):
    content_url: str = Field(
        max_length=250,
        schema_extra={"example": "https://www.example.com/dataset/file.csv"},
    )
    content_size_kb: int | None = Field(schema_extra={"example": 10000})
    description: str | None = Field(
        max_length=5000, schema_extra={"example": "Description of this file."}
    )
    encoding_format: str | None = Field(max_length=255, schema_extra={"example": "text/csv"})
    name: str | None = Field(max_length=150, schema_extra={"example": "Name of this file."})


class DataDownloadORM(DataDownloadBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "data_download"

    identifier: int | None = Field(primary_key=True)

    dataset_identifier: int | None = Field(
        sa_column=Column(Integer, ForeignKey("dataset.identifier", ondelete="CASCADE"))
    )
    checksum: List[ChecksumORM] = Relationship(
        back_populates="distribution", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    class RelationshipConfig:
        checksum: List[Checksum] = ResourceRelationshipList(
            deserializer=CastDeserializer(ChecksumORM)
        )


class DataDownload(DataDownloadBase):
    """All or part of a Dataset in downloadable form"""

    checksum: List["Checksum"] = Field(default_factory=list)
