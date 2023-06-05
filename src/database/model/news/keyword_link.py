from sqlmodel import SQLModel, Field


class NewsKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "news_keyword_link"
    news_identifier: int = Field(foreign_key="news.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
