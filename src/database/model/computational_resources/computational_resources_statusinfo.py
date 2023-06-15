from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.example import ComputationalResource

class ComputationalResourceStatusInfoEnumLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "type_enum_link"

    statusInfo: str = Field(max_length=1500, schema_extra={"example": "Web page providing additional information like monitoring aspects"})

    statusInfo_identifier: int = Field(foreign_key="statusInfo.identifier", primary_key=True)
    statusInfo_enum_identifier: int = Field(foreign_key="statusInfo_enum.identifier", primary_key=True)
