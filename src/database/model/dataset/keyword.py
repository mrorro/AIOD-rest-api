from sqlmodel import SQLModel, Field


class DatasetKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_keyword_link"
    dataset_identifier: int = Field(foreign_key="dataset.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
