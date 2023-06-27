from sqlalchemy import Integer, Column, ForeignKey
from sqlmodel import SQLModel, Field


class NewsBusinessCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "news_business_category_link"
    news_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("news.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
