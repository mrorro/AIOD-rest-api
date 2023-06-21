from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from database.model.agent_table import AgentTable
from database.model.ai_asset import AIAsset
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
    ComputationalResourceDistributionOrm,
)
from database.model.computational_resource.computational_resource_keyword_link import (
    ComputationalResourceKeywordLink,
)
from database.model.computational_resource.computational_resources_otherinfo import (
    ComputationalResourceOtherInfoLink,
    ComputationalResourceOtherInfo,
)
from database.model.computational_resource.contact_link import ComputationalResourceContactLink
from database.model.computational_resource.creator_link import ComputationalResourceCreatorLink
from database.model.computational_resource.managed_by_link import ComputationalResourceManagedByLink
from database.model.computational_resource.research_area_link import (
    ComputationalResourceResearchAreaLink,
)
from database.model.general.application_areas import ApplicationArea
from database.model.general.keyword import Keyword
from database.model.general.research_areas import ResearchArea
from database.model.computational_resource.uri import (
    ComputationalResourceUri,
    ComputationalResourceUriOrm,
)
from database.model.relationships import ResourceRelationshipList
from serialization import (
    CastDeserializer,
    FindByIdentifierDeserializer,
    FindByNameDeserializer,
    AttributeSerializer,
)


class ComputationalResourceParentChildLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "computational_resource_parent_child_link"
    parent_identifier: int = Field(
        foreign_key="computational_resource.identifier", primary_key=True
    )
    child_identifier: int = Field(foreign_key="computational_resource.identifier", primary_key=True)


class ComputationalResourceBase(AIAsset):
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

    identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")

    alternate_name: list[ComputationalResourceAlternateName] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceAlternateNameLink
    )
    capability: list[ComputationalResourceCapability] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCapabilityLink
    )
    citation: list[ComputationalResourceCitation] = Relationship(
        back_populates="computational_resources", link_model=ComputationalResourceCitationLink
    )
    distribution: list[ComputationalResourceDistributionOrm] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    statusInfo: list[ComputationalResourceUriOrm] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
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

    creator: list["AgentTable"] = Relationship(link_model=ComputationalResourceCreatorLink)
    contact: list["AgentTable"] = Relationship(link_model=ComputationalResourceContactLink)
    managedBy: list["AgentTable"] = Relationship(link_model=ComputationalResourceManagedByLink)
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
        creator: list[int] = ResourceRelationshipList(
            example=[],
            serializer=AttributeSerializer("identifier"),
            deserializer=FindByIdentifierDeserializer(AgentTable),
        )
        contact: list[int] = ResourceRelationshipList(
            example=[],
            serializer=AttributeSerializer("identifier"),
            deserializer=FindByIdentifierDeserializer(AgentTable),
        )
        managedBy: list[int] = ResourceRelationshipList(
            example=[],
            serializer=AttributeSerializer("identifier"),
            deserializer=FindByIdentifierDeserializer(AgentTable),
        )
        distribution: list[ComputationalResourceDistribution] = ResourceRelationshipList(
            deserializer=CastDeserializer(ComputationalResourceDistributionOrm)
        )
        statusInfo: list[ComputationalResourceUri] = ResourceRelationshipList(
            deserializer=CastDeserializer(ComputationalResourceUriOrm)
        )


# Defined separate because it references ComputationalResource,
# and can therefor not be defined inside ComputationalResource
deserializer = FindByIdentifierDeserializer(ComputationalResource)
ComputationalResource.RelationshipConfig.isPartOf.deserializer = deserializer  # type: ignore[attr-defined] # noqa E501
ComputationalResource.RelationshipConfig.hasPart.deserializer = deserializer  # type: ignore[attr-defined]  # noqa E501
