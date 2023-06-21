from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from database.model.computational_resource.application_area_link import (
    ComputationalResourceApplicationAreaLink,
)

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
    ComputationalResourceDistributionLink,
)
from database.model.computational_resource.computational_resource_keyword_link import (
    ComputationalResourceKeywordLink,
)
from database.model.computational_resource.computational_resources_otherinfo import (
    ComputationalResourceOtherInfoLink,
    ComputationalResourceOtherInfo,
)
from database.model.computational_resource.research_area_link import (
    ComputationalResourceResearchAreaLink,
)
from database.model.general.application_areas import ApplicationArea
from database.model.general.keyword import Keyword
from database.model.general.research_areas import ResearchArea
from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource
from serialization import FindByIdentifierDeserializer, FindByNameDeserializer, AttributeSerializer


class ComputationalResourceParentChildLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_parent_child_link"
    parent_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    child_identifier: int = Field(foreign_key="computational_resource.identifier", primary_key=True)


class ComputationalResourceBase(Resource):
    # Required fields

    # Recommended fields
    name: str | None = Field(max_length=150, schema_extra={"example": "Human-readable name"})
    description: str | None = Field(max_length=5000, schema_extra={"example": "description"})
    logo: str | None = Field(
        max_length=250,
        schema_extra={"example": "https://www.example.com/computational_resource/example"},
    )
    creationTime: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )
    validity: int | None = Field(default=None, schema_extra={"example": 22})
    complexity: str | None = Field(
        max_length=250,
        schema_extra={"example": "complexity example"},
    )
    location: str | None = Field(
        max_length=500, schema_extra={"example": "Example location Computational resource"}
    )
    type: str | None = Field(
        max_length=500, schema_extra={"example": "Example type Computational resource"}
    )

    qualityLevel: str | None = Field(
        max_length=500, schema_extra={"example": "Example quality level Computational resource"}
    )


class ComputationalResource(ComputationalResourceBase, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource"

    identifier: int = Field(default=None, primary_key=True)

    alternate_name: list[ComputationalResourceAlternateName] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceAlternateNameLink
    )
    capability: list[ComputationalResourceCapability] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCapabilityLink
    )
    citation: list[ComputationalResourceCitation] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCitationLink
    )
    distribution: list[ComputationalResourceDistribution] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceDistributionLink
    )
    keyword: list[Keyword] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceKeywordLink
    )
    other_info: list[ComputationalResourceOtherInfo] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceOtherInfoLink
    )
    research_area: list["ResearchArea"] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceResearchAreaLink
    )
    application_area: list["ApplicationArea"] = Relationship(
        back_populates="computational_resources",
        link_model=ComputationalResourceApplicationAreaLink,
    )
    # statusInfo: list[str] = Relationship(
    #     back_populates="examples", link_model=ComputationalResourceStatusInfoEnumLink
    # )

    hasPart: list["ComputationalResource"] = Relationship(
        back_populates="isPartOf",
        link_model=ComputationalResourceParentChildLink,
        sa_relationship_kwargs=dict(
            primaryjoin="ComputationalResource.identifier==ComputationalResourceParentChildLink.parent_identifier",  # noqa E501
            secondaryjoin="ComputationalResource.identifier==ComputationalResourceParentChildLink.child_identifier",  # noqa E501
        ),
    )
    isPartOf: list["ComputationalResource"] = Relationship(
        back_populates="hasPart",
        link_model=ComputationalResourceParentChildLink,
        sa_relationship_kwargs=dict(
            primaryjoin="ComputationalResource.identifier==ComputationalResourceParentChildLink.child_identifier",  # noqa E501
            secondaryjoin="ComputationalResource.identifier==ComputationalResourceParentChildLink.parent_identifier",  # noqa E501
        ),
    )

    class RelationshipConfig:  # This is AIoD-specific code, used to go from Pydantic to SqlAlchemy
        # otherInfo_enum: str | None = ResourceRelationshipSingle(
        #     identifier_name="otherInfo_enum_identifier",
        #     serializer=AttributeSerializer("otherInfo"),  # code to serialize ORM to Pydantic
        #     deserializer=FindByNameDeserializer(
        #         ComputationalResourceOtherInfoEnum
        #     ),  # deserialize Pydantic to ORM
        #     example="string: tag",
        # )

        alternate_name: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceAlternateName),
            description="",
        )
        capability: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceCapability),
            description="The provided capability according to the Open Grid Service Architecture ("
            "OGSA) architecture [OGF-GFD80]",
        )
        # Is there a URI type that we can reuse here instead of string?
        citation: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceCitation),
            description="A bibliographic reference for the AI asset.",
        )
        # here there's a type distribution set as string for now
        distribution: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceDistribution),
            description="A Distribution of the AI Asset",
        )
        keyword: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(Keyword),
            description="terms or phrases providing additional context for the AI asset.",
        )
        other_info: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ComputationalResourceOtherInfo),
            description="laceholder to publish info that does not fit in any other attribute. "
            "Free-form string, comma-separated tags, (name, value ) pair are all "
            "examples of valid syntax ",
        )
        research_area: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ResearchArea),
            example=["research_area1", "research_area2"],
        )
        application_area: list[str] = ResourceRelationshipList(
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(ApplicationArea),
            example=["application_area1", "application_area2"],
        )
        isPartOf: list[int] = ResourceRelationshipList(
            example=[],
            serializer=AttributeSerializer("identifier"),
        )
        hasPart: list[int] = ResourceRelationshipList(
            example=[],
            serializer=AttributeSerializer("identifier"),
        )
        #
        # statusInfo_enum: str | None = ResourceRelationshipSingle(
        #     identifier_name="statusInfo_identifier",
        #     serializer=AttributeSerializer("statusInfo"),  # code to serialize ORM to Pydantic
        #     deserializer=FindByNameDeserializer(
        #         ComputationalResourceStatusInfoEnum
        #     ),  # deserialize Pydantic to ORM
        #     example="",
        # )


# Defined separate because it references ComputationalResource,
# and can therefor not be defined inside ComputationalResource
deserializer = FindByIdentifierDeserializer(ComputationalResource)
ComputationalResource.RelationshipConfig.isPartOf.deserializer = deserializer  # type: ignore[attr-defined] # noqa E501
ComputationalResource.RelationshipConfig.hasPart.deserializer = deserializer  # type: ignore[attr-defined]  # noqa E501
