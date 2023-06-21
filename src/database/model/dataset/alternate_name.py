from typing import List
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset.dataset import Dataset


class DatasetAlternateNameLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_alternate_name_link"

    dataset_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("dataset.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    alternate_name_identifier: int | None = Field(
        foreign_key="dataset_alternate_name.identifier", primary_key=True
    )


class DatasetAlternateName(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_alternate_name"

    datasets: List["Dataset"] = Relationship(
        back_populates="alternate_names", link_model=DatasetAlternateNameLink
    )
