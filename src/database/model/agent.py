from sqlmodel import SQLModel, Field


class Agent(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "agent"

    """Every Organisation, member, etc. has a relationship to the Agent. They are thus separate
    models (which is different from the Metadata description) where all the fields of the
    AIAsset, such as name and description, are put on every asset themselves."""
    identifier: int = Field(
        default=None,
        primary_key=True,
        description="The identifier of each agent should be the same as this " "identifier",
    )
    type: str = Field(
        description="The name of the table of the asset. E.g. 'organisation' or " "'member'"
    )
