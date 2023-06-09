from sqlmodel import SQLModel, Field


class EducationalResourceBusinessCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educatioanal_resource_business_category_link"
    case_study_identifier: int = Field(
        foreign_key="educational_resource.identifier", primary_key=True
    )
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
