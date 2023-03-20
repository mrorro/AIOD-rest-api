from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
import datetime


class Dataset(BaseModel):
    """The complete metadata of a dataset. Possibly in schema.org format. For now, only a couple
    of fields are shown, we have to decide which fields to use."""

    name: str = Field(max_length=150)
    node: str = Field(max_length=30)
    node_specific_identifier: str = Field(max_length=250)
    id: int | None


class Publication(BaseModel):
    """The complete metadata of a publication. For now, only a couple of fields are shown,
    we have to decide which fields to use."""

    title: str = Field(max_length=250)
    url: str = Field(max_length=250)
    id: int | None


class Tag(BaseModel):
    """The complete metadata for tags"""

    tag: str = Field(max_length=250)
    id: int | None


class BusinessCategory(BaseModel):
    """The complete metadata of a business category"""

    category: str = Field(max_length=250)
    id: int | None


class NewsCategory(BaseModel):
    """The complete metadata of a news category"""

    category: str = Field(max_length=250)
    parent_id: int | None
    id: int | None


class MediaEnum(str, Enum):
    books = "books"
    Eclipse = "Eclipse"
    education = "education"
    library = "library"


class News(BaseModel):
    """The complete metadata for news entity"""

    title: str = Field(max_length=500)
    date: datetime.date
    body: str = Field(max_length=2000)
    media: Optional[MediaEnum]
    source: Optional[str]
    news_categories: Optional[list[str]]
    business_categories: Optional[list[str]]
    tags: Optional[list[str]]
    id: int | None
