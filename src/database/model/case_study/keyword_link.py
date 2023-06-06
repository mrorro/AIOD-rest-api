from sqlmodel import SQLModel, Field


class CaseStudyKeywordLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_keyword_link"
    case_study_identifier: int = Field(foreign_key="case_study.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="keyword.identifier", primary_key=True)
