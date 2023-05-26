from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship, SQLModel, Field

from database.model.named_relation import NamedRelation
from database.model.resource import ResourceRelationship
from database.serialization import AttributeSerializer, FindByNameDeserializer, create_getter_dict

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset.data_download import DataDownloadORM


class ChecksumAlgorithm(NamedRelation, table=True):  # type: ignore [call-arg]
    """A checksum algorithm (such as MD5)"""

    __tablename__ = "checksum_algorithm"

    checksums: List["ChecksumORM"] = Relationship(back_populates="algorithm")


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
    distribution_identifier: int | None = Field(foreign_key="data_download.identifier")
    distribution: "DataDownloadORM" = Relationship(back_populates="checksum")

    class RelationshipConfig:
        algorithm: str | None = ResourceRelationship(
            identifier_name="algorithm_identifier",
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ChecksumAlgorithm),
            example="md5",
        )


class Checksum(ChecksumBase):
    algorithm: str = Field(schema_extra={"example": "md5"})

    class Config:
        getter_dict = create_getter_dict({"algorithm": AttributeSerializer("name")})
