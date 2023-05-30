from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset.checksum import ChecksumORM


class ChecksumAlgorithm(NamedRelation, table=True):  # type: ignore [call-arg]
    """A checksum algorithm (such as MD5)"""

    __tablename__ = "checksum_algorithm"

    checksums: List["ChecksumORM"] = Relationship(back_populates="algorithm")
