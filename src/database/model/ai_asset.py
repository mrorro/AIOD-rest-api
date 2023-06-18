from sqlmodel import SQLModel, Field


class AIAsset(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "ai_asset"

    """Every Dataset, Publication, etc. has a relationship to the AIAsset. They are thus separate
    models (which is different from the Metadata description) where all the fields of the
    AIAsset, such as name and description, are put on every asset themselves."""
    identifier: int = Field(
        default=None,
        primary_key=True,
        description="The identifier of each asset should be the same as this identifier",
    )
    type: str = Field(
        description="The name of the table of the asset. E.g. 'dataset' or 'publication'"
    )
