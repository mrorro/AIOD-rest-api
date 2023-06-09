from sqlmodel import SQLModel, Field


class AgentTable(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "agent_table"

    """Every Organisation, member, etc. has a relationship to the Agent.
    The agent_table defines this relationship"""
    identifier: int = Field(
        default=None,
        primary_key=True,
        description="The identifier of each agent should be the same as this " "identifier",
    )
    type: str = Field(
        description="The name of the table of the asset. E.g. 'organisation' or " "'member'"
    )
