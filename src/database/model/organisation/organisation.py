from datetime import datetime

# from typing import List
from sqlmodel import Field

# from database.model.general.keyword import Keyword
# from database.model.general.business_category import BusinessCategory
# from database.model.news.keyword_link import NewsKeywordLink
# from database.model.news.media_link import NewsMediaLink
# from database.model.news.news_category_link import NewsCategoryNewsLink
# from database.model.relationships import ResourceRelationshipList
from database.model.resource import Resource

# from serialization import (
#     AttributeSerializer,
#     FindByNameDeserializer,
# )


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
        max_length=500, default=None, schema_example={"example": "Example official name"}
    )
    alternate_name: str | None = Field(
        max_length=500, default=None, schema_example={"example": "Example alternate name"}
    )
    address: str | None = Field(
        max_length=500, default=None, schema_example={"example": "Example address"}
    )
    telephone: str | None = Field(
        max_length=500, default=None, schema_example={"example": "Example telephone number"}
    )
    parent_organisation_id: int | None = Field(
        foreign_key="organisations.identifier",
        default=None,
        schema_example={"example": "Example parent organisation 1"},
    )
    subsidiary_organisation_id: int | None = Field(
        foreign_key="organisations.identifier",
        default=None,
        schema_example={"example": "Example subsidiary organisation 1"},
    )


# class Organisation(OrganisationBase, table=True):  # type: ignore
#     __tablename__ = "organisation"

#     identifier: int = Field(primary_key=True, foreign_key="ai_asset.identifier")

#     business_categories: List[BusinessCategory] = Relationship(
#         back_populates="organisations", link_model=OrganisationBusinessCategoryLink
#     )
#     technical_categories: List[TechnicalCategory] = Relationship(
#         back_populates="organisations", link_model=OrganisationTechnicalCategoryLink
#     )
#     email_address: List[Email] = Relationship(
#         sa_relationship_kwargs={"cascade", "all, delete-orphan"}
#     )
#     members: list[Agent] = Relationship(
#         back_populates="members",
#         sa_relationship_kwargs={"passive_deletes": "all"},
#         link_model=OrganisationMember,
#     )
#     departments: List[Agent] = Relationship(
#         back_populates="departments",
#         sa_relationship_kwargs={"passive_deletes": "all"},
#         link_model=OrganisationDepartment,
#     )

#     class RelationshipConfig:

#         business_categories: List[str] = ResourceRelationshipList(
#             example=["business category 1", "business category 2"],
#             serializer=AttributeSerializer("name"),
#             deserializer=FindByNameDeserializer(BusinessCategory),
#         )
#         technical_categories: List[str] = ResourceRelationshipList(
#             example=["technical category 1", "technical category 2"],
#             serializer=AttributeSerializer("name"),
#             deserializer=FindByNameDeserializer(TechnicalCategory),
#         )
