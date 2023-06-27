from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class OrganisationTechnicalCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_technical_category_link"
    organisation_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("organisation.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    technical_category_identifier: int = Field(
        foreign_key="technical_category.identifier", primary_key=True
    )
