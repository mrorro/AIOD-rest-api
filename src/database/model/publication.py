from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.ai_resource import OrmAIResource
from database.model.dataset_relationships import dataset_publication_relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset import OrmDataset


class OrmPublication(OrmAIResource):
    """Any publication."""

    __tablename__ = "publications"

    identifier: Mapped[int] = mapped_column(
        ForeignKey("ai_resources.identifier"), init=False, primary_key=True
    )

    title: Mapped[str] = mapped_column(String(250), nullable=False)
    doi: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    creators: Mapped[str] = mapped_column(String(450), nullable=True, default=None)
    access_right: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    license: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    publication_type: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    date_published: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    notes: Mapped[str] = mapped_column(String(450), nullable=True, default=None)
    url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)

    datasets: Mapped[list["OrmDataset"]] = relationship(
        default_factory=list,
        back_populates="citations",
        secondary=dataset_publication_relationship,
    )

    __mapper_args__ = {
        "polymorphic_identity": "publication",
        "inherit_condition": identifier == OrmAIResource.identifier,
    }
