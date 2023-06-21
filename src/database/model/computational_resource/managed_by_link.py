from sqlmodel import SQLModel, Field


class ComputationalResourceManagedByLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_managed_by_link"
    computational_resource_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    agent_identifier: int = Field(foreign_key="agent.identifier", primary_key=True)
