from sqlmodel import SQLModel, Field


class EducationalResourceLanguageLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educational_resource_language_link"
    dataset_identifier: int = Field(foreign_key="educational_resource.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="language.identifier", primary_key=True)
