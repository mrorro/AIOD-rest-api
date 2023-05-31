from sqlmodel import SQLModel, Field


class CaseStudyBusinessCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_business_category_link"
    case_study_identifier: int = Field(foreign_key="case_study.identifier", primary_key=True)
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
