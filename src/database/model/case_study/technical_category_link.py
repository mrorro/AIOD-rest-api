from sqlalchemy import Integer, Column, ForeignKey
from sqlmodel import SQLModel, Field


class CaseStudyTechnicalCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_technical_category_link"
    casestudy_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("case_study.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    technical_category_identifier: int = Field(
        foreign_key="technical_category.identifier", primary_key=True
    )
