from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.base import Base
from database.model.dataset_relationships import dataset_publication_relationship

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset import OrmDataset


class OrmPublication(Base):
    """Any publication."""

    __tablename__ = "publications"
    __table_args__ = (
        UniqueConstraint(
            "node",
            "node_specific_identifier",
            name="publication_unique_node_node_specific_identifier",
        ),
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    doi: Mapped[str] = mapped_column(String(150), nullable=False)
    node: Mapped[str] = mapped_column(String(30), nullable=False)
    node_specific_identifier: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datasets: Mapped[list["OrmDataset"]] = relationship(
        default_factory=list,
        back_populates="citations",
        secondary=dataset_publication_relationship,
    )
