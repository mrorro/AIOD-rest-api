from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class NewsCategoryNewsLink(SQLModel, table=True):  # type: ignore [call-arg]
    _tablename_ = "news_category_news_link"
    news_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("news.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    news_categories_identifier: int = Field(
        foreign_key="news_category.identifier", primary_key=True
    )
