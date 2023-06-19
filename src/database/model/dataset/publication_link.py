from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class DatasetPublicationLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_publication_link"
    dataset_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("dataset.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    publication_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("publication.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
