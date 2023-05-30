from sqlmodel import SQLModel, Field


class DatasetPublicationLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_publication_link"
    dataset_identifier: int = Field(foreign_key="dataset.identifier", primary_key=True)
    publication_identifier: int = Field(foreign_key="publication.identifier", primary_key=True)
