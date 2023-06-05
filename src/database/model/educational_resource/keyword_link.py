from sqlmodel import SQLModel, Field


class EducationalResourceKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educational_resource_keyword_link"
    educational_resource_identifier: int = Field(
        foreign_key="educational_resource.identifier", primary_key=True
    )
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
