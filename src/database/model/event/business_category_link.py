from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class EventBusinessCategoriesLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "event_business_category_link"
    event_identifier: int = Field(
        sa_column=Column(
            Integer, ForeignKey("event.identifier", ondelete="CASCADE"), primary_key=True
        )
    )
    business_category_identifier: int = Field(
        foreign_key="business_category.identifier", primary_key=True
    )
