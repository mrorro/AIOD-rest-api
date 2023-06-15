# from typing import TYPE_CHECKING
#
# from sqlmodel import SQLModel, Field
#
# if TYPE_CHECKING:  # avoid circular imports; only import while type checking
#     from database.model.example import ComputationalResource
#
#
# class ComputationalResourceTypeEnumLink(SQLModel, table=True):  # type: ignore [call-arg]
#     __tablename__ = "type_enum_link"
#
#     #type: str = Field(
#         max_length=1500,
#         schema_extra={
#             "example": "The type of service according to a namespace-based classification (the "
#                        "namespace MAY be related to a middleware name, an organization or other "
#                        "concepts; org.ogf.glue is reserved for the OGF GLUE Working Group)"
#         },
#     )
#
#     type_identifier: int = Field(foreign_key="type.identifier", primary_key=True)
#     type_enum_identifier: int = Field(foreign_key="type_enum.identifier", primary_key=True)
