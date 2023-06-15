from datetime import datetime

from sqlmodel import Field, Relationship

from database.model.computational_resource.computational_resource_capability import (
    ComputationalResourceCapabilityLink,
    ComputationalResourceCapability,
)
from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource
from serialization import FindByNameDeserializer, AttributeSerializer


class ComputationalResourceBase(Resource):
    # Required fields

    # Recommended fields
    validity: int | None = Field(default=None, schema_extra={"example": 22})
    name: str = Field(max_length=150, schema_extra={"example": "Human-readable name"})

    creationTime: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )

    qualityLevel: str = Field(
        max_length=150,
        schema_extra={"example": "TODO"},
    )

    complexity: str = Field(
        max_length=150,
        description="Human-readable summary description of the complexity in terms of the number "
        "of endpoint types, shares and resources. The syntax should be: "
        "endpointType=X, share=Y, resource=Z.",
        schema_extra={"example": "endpointType=X, share=Y, resource=Z."},
    )


class ComputationalResource(ComputationalResourceBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource"

    identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")

    # otherInfo: list[str] = Relationship(
    #     back_populates="examples", link_model=ComputationalResourceOtherInfoEnumLink
    # )
    capability: list[str] = Relationship(
        back_populates="examples", link_model=ComputationalResourceCapabilityLink
    )
    # #type: list[str] = Relationship(
    #     back_populates="examples", link_model=ComputationalResourceTypeEnumLink
    # )
    # statusInfo: list[str] = Relationship(
    #     back_populates="examples", link_model=ComputationalResourceStatusInfoEnumLink
    # )

    class RelationshipConfig:  # This is AIoD-specific code, used to go from Pydantic to SqlAlchemy
        # otherInfo_enum: str | None = ResourceRelationshipSingle(
        #     identifier_name="otherInfo_enum_identifier",
        #     serializer=AttributeSerializer("otherInfo"),  # code to serialize ORM to Pydantic
        #     deserializer=FindByNameDeserializer(
        #         ComputationalResourceOtherInfoEnum
        #     ),  # deserialize Pydantic to ORM
        #     example="string: tag",
        # )

        capability: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceCapability),
            description="The provided capability according to the Open Grid Service Architecture ("
            "OGSA) architecture [OGF-GFD80]",
        )

        # type_enum: str | None = ResourceRelationshipSingle(
        #     identifier_name="type_identifier",
        #     serializer=AttributeSerializer("type"),  # code to serialize ORM to Pydantic
        #     deserializer=FindByNameDeserializer(
        #         ComputationalResourceTypeEnum
        #     ),  # deserialize Pydantic to ORM
        #     example="Maturity of the service in terms of quality of the software components",
        # )
        #
        # statusInfo_enum: str | None = ResourceRelationshipSingle(
        #     identifier_name="statusInfo_identifier",
        #     serializer=AttributeSerializer("statusInfo"),  # code to serialize ORM to Pydantic
        #     deserializer=FindByNameDeserializer(
        #         ComputationalResourceStatusInfoEnum
        #     ),  # deserialize Pydantic to ORM
        #     example="",
        # )
