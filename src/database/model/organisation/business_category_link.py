from sqlmodel import SQLModel, Field


class OrganisationBusinessCategoryLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_business_category_link"
    organisation_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
