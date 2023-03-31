from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.ai_resource import OrmAIResource
from database.model.dataset_relationships import dataset_publication_relationship

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset import OrmDataset


class OrmPublication(OrmAIResource):
    """Any publication."""

    __tablename__ = "publications"
    __table_args__ = (
        UniqueConstraint(
            "platform",
            "platform_identifier",
            name="publication_unique_platform_platform_identifier",
        ),
    )

    title: Mapped[str] = mapped_column(String(250), nullable=False)
    doi: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    datasets: Mapped[list["OrmDataset"]] = relationship(
        default_factory=list,
        back_populates="citations",
        secondary=dataset_publication_relationship,
    )
