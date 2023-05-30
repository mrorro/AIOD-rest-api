from typing import List
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset.dataset import Dataset


class DatasetMeasuredValueNameLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "dataset_measured_value_link"

    dataset_identifier: int = Field(foreign_key="dataset.identifier", primary_key=True)
    measured_value_identifier: int = Field(
        foreign_key="measured_value.identifier", primary_key=True
    )


class MeasuredValue(SQLModel):
    """The variable that this dataset measures. For example, temperature or pressure, including the
    technique, technology, or methodology used in a dataset"""

    variable: str = Field(max_length=150, schema_extra={"example": "molecule concentration"})
    technique: str = Field(max_length=150, schema_extra={"example": "mass spectrometry"})


class MeasuredValueORM(MeasuredValue, table=True):  # type: ignore [call-arg]
    __tablename__ = "measured_value"
    __table_args__ = (
        UniqueConstraint(
            "variable",
            "technique",
            name="measuredValue_variable_technique",
        ),
    )
    identifier: int | None = Field(primary_key=True)
    datasets: List["Dataset"] = Relationship(
        back_populates="measured_values", link_model=DatasetMeasuredValueNameLink
    )
