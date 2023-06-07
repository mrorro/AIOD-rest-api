from datetime import datetime

from typing import List
from sqlmodel import Field, Relationship, SQLModel

from database.model.agent import Agent

from database.model.organisation.email import (
    OrganisationEmail,
    OrganisationEmailLink,
)

from database.model.general.business_category import BusinessCategory
from database.model.organisation.business_category_link import OrganisationBusinessCategoryLink

from database.model.general.technical_category import TechnicalCategory
from database.model.organisation.technical_category_link import OrganisationTechnicalCategoryLink

from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource

from database.model.organisation.member_link import OrganisationMemberLink
from database.model.organisation.department_link import OrganisationDepartmentLink

from serialization import AttributeSerializer, FindByNameDeserializer, FindByIdentifierDeserializer


class OrganisationParentChildLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_parent_child_link"
    parent_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)
    child_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)


class OrganisationBase(Resource):
    # Required fields
    type: str = Field(max_length=500, schema_extra={"example": "Example Research Insititution"})

    # Recommended fields
    connection_to_ai: str | None = Field(
        max_length=50,
        default=None,
        schema_extra={"example": "Example description of positioning in European AI ecosystem."},
    )
    logo_url: str | None = Field(
        max_length=50, default=None, schema_extra={"example": "aiod.eu/project/0/logo"}
    )
    same_as: str | None = Field(
        max_length=150,
        unique=True,
        schema_extra={"example": "https://www.example.com/organisation/example"},
    )
    founding_date: datetime | None = Field(
        default=None, schema_extra={"example": "2022-01-01T15:15:00.000Z"}
    )
    dissolution_date: datetime | None = Field(
        default=None, schema_extra={"example": "2023-01-01T15:15:00.000Z"}
    )
    legal_name: str | None = Field(
        max_length=500, default=None, schema_extra={"example": "Example official name"}
    )
    alternate_name: str | None = Field(
        max_length=500, default=None, schema_extra={"example": "Example alternate name"}
    )
    address: str | None = Field(
        max_length=500, default=None, schema_extra={"example": "Example address"}
    )
    telephone: str | None = Field(
        max_length=500, default=None, schema_extra={"example": "Example telephone number"}
    )
    parent_organisation_id: int | None = Field(
        foreign_key="organisation.identifier",
        default=None,
        schema_extra={"example": 1},
    )
    subsidiary_organisation_id: int | None = Field(
        foreign_key="organisation.identifier",
        default=None,
        schema_extra={"example": 2},
    )


class Organisation(OrganisationBase, table=True):  # type: ignore
    __tablename__ = "organisation"

    identifier: int = Field(primary_key=True, foreign_key="agent.identifier")

    business_categories: List[BusinessCategory] = Relationship(
        back_populates="organisations", link_model=OrganisationBusinessCategoryLink
    )
    technical_categories: List[TechnicalCategory] = Relationship(
        back_populates="organisations", link_model=OrganisationTechnicalCategoryLink
    )
    emails: List[OrganisationEmail] = Relationship(
        back_populates="organisations", link_model=OrganisationEmailLink
    )
    members: list[Agent] = Relationship(
        link_model=OrganisationMemberLink,
    )
    departments: List[Agent] = Relationship(
        link_model=OrganisationDepartmentLink,
    )

    class RelationshipConfig:

        business_categories: List[str] = ResourceRelationshipList(
            example=["business category 1", "business category 2"],
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(BusinessCategory),
        )
        technical_categories: List[str] = ResourceRelationshipList(
            example=["technical category 1", "technical category 2"],
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(TechnicalCategory),
        )
        emails: List[str] = ResourceRelationshipList(
            example=["email@org.com"],
            serializer=AttributeSerializer("name"),
            deserializer=FindByNameDeserializer(OrganisationEmail),
        )
        members: List[int] = ResourceRelationshipList(
            example=[1, 2],
            serializer=AttributeSerializer("identifier"),
            deserializer=FindByIdentifierDeserializer(Agent),
        )

        departments: List[int] = ResourceRelationshipList(
            example=[1, 2],
            serializer=AttributeSerializer("identifier"),
            deserializer=FindByIdentifierDeserializer(Agent),
        )


# Defined separate because it references Organisation,
# and can therefor not be defined inside Organisation
deserializer = FindByIdentifierDeserializer(Organisation)
