from sqlmodel import SQLModel, Field


class EducationalResourceTargetAudienceLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "educational_resource_target_audience_link"
    dataset_identifier: int = Field(foreign_key="educational_resource.identifier", primary_key=True)
    keyword_identifier: int = Field(foreign_key="target_audience.identifier", primary_key=True)
