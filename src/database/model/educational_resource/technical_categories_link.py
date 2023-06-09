from sqlmodel import SQLModel, Field


class EducationalResourceTechnicalCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educatioanal_resource_technical_category_link"
    case_study_identifier: int = Field(
        foreign_key="educational_resource.identifier", primary_key=True
    )
    technical_category_identifier: int = Field(
        foreign_key="technical_category.identifier", primary_key=True
    )
