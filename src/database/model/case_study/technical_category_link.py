from sqlmodel import SQLModel, Field


class CaseStudyTechnicalCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_technical_category_link"
    case_study_identifier: int = Field(foreign_key="case_study.identifier", primary_key=True)
    technical_category_identifier: int = Field(
        foreign_key="technical_category.identifier", primary_key=True
    )
