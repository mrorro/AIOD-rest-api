from datetime import datetime

from sqlmodel import Field, Relationship

from database.model.computational_resource.computational_resource_alternate_name import (
    ComputationalResourceAlternateNameLink,
    ComputationalResourceAlternateName,
)
from database.model.computational_resource.computational_resource_capability import (
    ComputationalResourceCapabilityLink,
    ComputationalResourceCapability,
)
from database.model.computational_resource.computational_resource_citation import (
    ComputationalResourceCitationLink,
    ComputationalResourceCitation,
)
from database.model.computational_resource.computational_resource_distribution import (
    ComputationalResourceDistribution,
)
from database.model.computational_resource.computational_resource_keyword import (
    ComputationalResourceKeywordLink,
    ComputationalResourceKeyword,
)
from database.model.computational_resource.computational_resources_otherinfo import (
    ComputationalResourceOtherInfoLink,
    ComputationalResourceOtherInfo,
)
from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource
from serialization import FindByNameDeserializer, AttributeSerializer


class ComputationalResourceBase(Resource):
    # Required fields

    # Recommended fields
    validity: int | None = Field(default=None, schema_extra={"example": 22})
    name: str = Field(max_length=150, schema_extra={"example": "Human-readable name"})
    description: str = Field(max_length=1500, schema_extra={"example": "description"})
    platform: str = Field(
        max_length=1500,
        schema_extra={"example": "The platform from which " "this AI Asset originates"},
    )
    platformIdentifier: str = Field(
        max_length=150,
        schema_extra={
            "example": "The identifier " "used to denote this AI asset in its originating platform"
        },
    )

    creationTime: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )

    qualityLevel: str = Field(
        max_length=150,
        description="The type of service according to a namespace-based "
        "classification (the namespace MAY be related to a middleware name, an organization "
        "or other concepts; org.ogf.glue is reserved for the OGF GLUE Working Group)",
        schema_extra={"example": ""},
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
    #     back_populates="computational_resources",
    #     link_model=ComputationalResourceOtherInfoEnumLink
    # )
    alternateName: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceAlternateNameLink
    )
    distribution: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceAlternateNameLink
    )
    keyword: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceKeywordLink
    )
    citation: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCitationLink
    )

    otherInfo: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceOtherInfoLink
    )
    capability: list[str] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCapabilityLink
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

        alternateName: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceAlternateName),
            description="",
        )

        # here there's a type distribution set as string for now
        distribution: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceDistribution),
            description="A Distribution of the AI Asset",
        )
        keyword: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceKeyword),
            description="terms or phrases providing additional context for the AI asset.",
        )
        # Is there a URI type that we can reuse here instead of string?
        citation: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceCitation),
            description="A bibliographic reference for the AI asset.",
        )

        otherInfo: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceOtherInfo),
            description="laceholder to publish info that does not fit in any other attribute. "
            "Free-form string, comma-separated tags, (name, value ) pair are all examples of "
            "valid syntax ",
        )
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
