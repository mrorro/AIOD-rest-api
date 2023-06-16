from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.computational_resource.computational_resource import ComputationalResource


class ComputationalResourceAlternateNameLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_alternate_name_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    alternate_name_identifier: int = Field(
        foreign_key="computational_resource_alternate_name.identifier", primary_key=True
    )


class ComputationalResourceAlternateName(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_alternate_name"
    computational_resources: List["ComputationalResource"] = Relationship(
        back_populates="alternate_name", link_model=ComputationalResourceAlternateNameLink
    )
