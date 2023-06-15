from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.computational_resource.computational_resource import ComputationalResource


class ComputationalResourceCapabilityLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_capability_link"
    capability_identifier: int = Field(foreign_key="capability.identifier", primary_key=True)
    capability_enum_identifier: int = Field(
        foreign_key="computational_resource_capability.identifier", primary_key=True
    )


class ComputationalResourceCapability(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_capability"
    computational_resources: List["ComputationalResource"] = Relationship(
        back_populates="capabilities", link_model=ComputationalResourceCapabilityLink
    )
