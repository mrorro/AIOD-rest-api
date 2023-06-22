from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    pass


class ComputationalResourceKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_keyword_link"
    computational_resource_identifier: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("computational_resource.identifier", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
