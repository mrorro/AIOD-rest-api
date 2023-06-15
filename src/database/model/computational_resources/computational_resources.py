from sqlmodel import Field
from database.model.resource import Resource

class ComputationalResourceBase(Resource):
    # Required fields


    # Recommended fields
    validity: int | None = Field(default=None, schema_extra={"example": 22})
    name: str = Field(max_length=150, schema_extra={"example": "Human-readable name"})
    otherInfo: List[OtherInfoEnum] = Relationship(
        back_populates="examples", link_model=ComputationalResourceOtherInfoEnumLink
    )
    capability: List[CapabilityEnum] = Relationship(
        back_populates="examples", link_model=ComputationalResourceCapabilityEnumLink
    )
    type: List[typeEnum] = Relationship(
        back_populates="examples", link_model=ComputationalResourceTypeEnumLink
    )

    QualityLevel: str = Field(max_length=150, schema_extra={"example": "Web page providing additional information like monitoring aspects"})

    statusInfo: List[typeEnum] = Relationship(
        back_populates="examples", link_model=ComputationalResourceStatusInfoEnumLink
    )

    complexity: str = Field(max_length=150, schema_extra={"example": "Human-readable summary description of the complexity in terms of the number of endpoint types, shares and resources. The syntax should be: endpointType=X, share=Y, resource=Z."})


class ComputationalReource(ComputationalReourceBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "computationalresource"
    __table_args__ = (
        UniqueConstraint(
            "string_field",
            "int_field",
            name="example_string_int_unique",  # A unique constraint on multiple columns
        ),
    )

    id: int = Field(primary_key=True, foreign_key="ai_asset.identifier")
    CreationTime: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )


    class RelationshipConfig:  # This is AIoD-specific code, used to go from Pydantic to SqlAlchemy
        otherInfo_enum: str | None = ResourceRelationshipSingle(
            identifier_name="otherInfo_enum_identifier",
            serializer=AttributeSerializer("otherInfo"),  # code to serialize ORM to Pydantic
            deserializer=FindByNameDeserializer(ComputationalResourceOtherInfoEnum),  # deserialize Pydantic to ORM
            example="string: tag",
        )

        capability_enum: str | None = ResourceRelationshipSingle(
            identifier_name="capability_identifier",
            serializer=AttributeSerializer("capability"),  # code to serialize ORM to Pydantic
            deserializer=FindByNameDeserializer(ComputationalResourceCapabilityEnum),  # deserialize Pydantic to ORM
            example="The provided capability according to the Open Grid Service Architecture (OGSA) architecture [OGF-GFD80]",
        )

        type_enum: str | None = ResourceRelationshipSingle(
            identifier_name="type_identifier",
            serializer=AttributeSerializer("type"),  # code to serialize ORM to Pydantic
            deserializer=FindByNameDeserializer(ComputationalResourceTypeEnum),  # deserialize Pydantic to ORM
            example="Maturity of the service in terms of quality of the software components",
        )

        statusInfo_enum: str | None = ResourceRelationshipSingle(
            identifier_name="statusInfo_identifier",
            serializer=AttributeSerializer("statusInfo"),  # code to serialize ORM to Pydantic
            deserializer=FindByNameDeserializer(ComputationalResourceStatusInfoEnum),  # deserialize Pydantic to ORM
            example="",
        )

