from pydantic import BaseModel, Field


class Dataset(BaseModel):
    """The complete metadata of a dataset. Possibly in schema.org format. For now, only a couple
    of fields are shown, we have to decide which fields to use.

    TODO(Jos): extent, corresponding to the Database variant, and update the PUT requests etc.
    """

    name: str = Field(max_length=150)
    description: str = Field(max_length=5000)
    same_as: str = Field(max_length=150)
    node: str = Field(max_length=30)
    node_specific_identifier: str = Field(max_length=250)
    id: int | None


class Publication(BaseModel):
    """The complete metadata of a publication. For now, only a couple of fields are shown,
    we have to decide which fields to use."""

    title: str = Field(max_length=250)
    url: str = Field(max_length=250)
    id: int | None
