from sqlmodel import SQLModel, Field


class ProjectKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "project_keyword_link"
    project_identifier: int = Field(foreign_key="project.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
