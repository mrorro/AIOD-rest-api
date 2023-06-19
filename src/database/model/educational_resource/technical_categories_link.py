from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class EducationalResourceTechnicalCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educational_resource_technical_category_link"
    educational_resource_identifier: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("educational_resource.identifier", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    technical_category_identifier: int = Field(
        foreign_key="technical_category.identifier", primary_key=True
    )
