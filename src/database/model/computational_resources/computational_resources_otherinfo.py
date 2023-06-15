from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.example import ComputationalResource

class ComputationalResourceOtherInfoEnumLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "otherInfo_enum_link"

    otherInfo: str = Field(max_length=150, schema_extra={"example": "Placeholder to publish info that does not fit in any other attribute. Free-form string, comma-separated tags, (name, value ) pair are all examples of valid syntax"})

    otherInfo_identifier: int = Field(foreign_key="otherInfo.identifier", primary_key=True)
    otherInfo_enum_identifier: int = Field(foreign_key="otherInfo_enum.identifier", primary_key=True)
