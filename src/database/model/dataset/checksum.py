from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import Relationship, SQLModel, Field

from database.model.dataset.checksum_algorithm import ChecksumAlgorithm
from database.model.relationships import ResourceRelationshipSingle
from serialization import AttributeSerializer, FindByNameDeserializer, create_getter_dict

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset.data_download import DataDownloadORM


class ChecksumBase(SQLModel):
    value: str = Field(max_length=500, schema_extra={"example": "123456789abcdefg123456789abcdefg"})


class ChecksumORM(ChecksumBase, table=True):  # type: ignore [call-arg]
    """
    A checksum.
    """

    __tablename__ = "checksum"

    identifier: int | None = Field(primary_key=True)
    algorithm_identifier: int | None = Field(foreign_key="checksum_algorithm.identifier")
    algorithm: ChecksumAlgorithm | None = Relationship(back_populates="checksums")
    distribution_identifier: int | None = Field(
        sa_column=Column(Integer, ForeignKey("data_download.identifier", ondelete="CASCADE"))
    )
    distribution: "DataDownloadORM" = Relationship(back_populates="checksum")

    class RelationshipConfig:
        algorithm: str | None = ResourceRelationshipSingle(
            identifier_name="algorithm_identifier",
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ChecksumAlgorithm),
            example="md5",
        )


class Checksum(ChecksumBase):
    algorithm: str = Field(schema_extra={"example": "md5"})

    class Config:
        getter_dict = create_getter_dict({"algorithm": AttributeSerializer("name")})
