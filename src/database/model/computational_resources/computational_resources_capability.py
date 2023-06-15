from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.example import ComputationalResource

class ComputationalResourceCapabilityEnumLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "capability_enum_link"

    capability: str = Field(max_length=150, schema_extra={"example": "The provided capability according to the Open Grid Service Architecture (OGSA) architecture [OGF-GFD80]"})

    capability_identifier: int = Field(foreign_key="capability.identifier", primary_key=True)
    capability_enum_identifier: int = Field(foreign_key="capability_enum.identifier", primary_key=True)
