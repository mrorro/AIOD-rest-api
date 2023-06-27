from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class NewsMediaLink(SQLModel, table=True):  # type: ignore [call-arg]
    _tablename_ = "news_media_link"
    news_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("news.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    media_identifier: int = Field(foreign_key="media.identifier", primary_key=True)
