from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class CaseStudyBusinessCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_business_category_link"
    casestudy_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("case_study.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
