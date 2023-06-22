from sqlmodel import SQLModel, Field


class NamedRelation(SQLModel):
    identifier: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="The string value")
