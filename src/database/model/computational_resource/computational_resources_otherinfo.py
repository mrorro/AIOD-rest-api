from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.computational_resource.computational_resource import ComputationalResource


class ComputationalResourceOtherInfoLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_other_info_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    other_info_identifier: int = Field(
        foreign_key="computational_resource_other_info.identifier", primary_key=True
    )


class ComputationalResourceOtherInfo(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_other_info"
    computational_resources: List["ComputationalResource"] = Relationship(
        back_populates="other_info", link_model=ComputationalResourceOtherInfoLink
    )
