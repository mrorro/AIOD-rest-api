from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.computational_resource.computational_resource import ComputationalResource


class ComputationalResourceDistributionLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_distribution_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    distribution_identifier: int = Field(
        foreign_key="computational_resource_distribution.identifier", primary_key=True
    )


class ComputationalResourceDistribution(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_distribution"
    computational_resources: List["ComputationalResource"] = Relationship(
        back_populates="distribution", link_model=ComputationalResourceDistributionLink
    )
