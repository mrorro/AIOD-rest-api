from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class ComputationalResourceHasShareLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_has_share_link"
    computational_resource_identifier: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("computational_resource.identifier", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    agent_identifier: int = Field(
        foreign_key="computational_resource_uri.identifier", primary_key=True
    )
