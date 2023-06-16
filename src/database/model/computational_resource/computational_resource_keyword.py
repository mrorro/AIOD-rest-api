from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.computational_resource.computational_resource import ComputationalResource


class ComputationalResourceKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_keyword_link"
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
    keyword_enum_identifier: int = Field(
        foreign_key="computational_resource_keyword.identifier", primary_key=True
    )


class ComputationalResourceKeyword(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_keyword"
    computational_resources: List["ComputationalResource"] = Relationship(
        back_populates="keyword", link_model=ComputationalResourceKeywordLink
    )
