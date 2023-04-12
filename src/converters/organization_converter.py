"""
Converting between different organization representations
"""
from sqlalchemy.orm import Session
from converters.conversion_helpers import retrieve_related_objects_by_ids

from converters.abstract_converter import ResourceConverter
from database.model.agent import OrmEmail
from database.model.general import OrmBusinessCategory, OrmTechnicalCategory
from database.model.organization import OrmOrganization
from schemas import AIoDOrganization


class OrganizationResourceConverter(ResourceConverter[AIoDOrganization, OrmOrganization]):
    def aiod_to_orm(
        self, session: Session, aiod: AIoDOrganization, return_existing_if_present: bool = False
    ) -> OrmOrganization:
        """
        Converting between organization representations:
        the AIoD schema towards the database variant
        """
        members = retrieve_related_objects_by_ids(session, aiod.members, OrmOrganization)
        departments = retrieve_related_objects_by_ids(session, aiod.departments, OrmOrganization)

        return OrmOrganization.create_or_get(
            session=session,
            create=not return_existing_if_present,
            platform=aiod.platform,
            platform_identifier=aiod.platform_identifier,
            name=aiod.name,
            description=aiod.description,
            image_url=aiod.image_url,
            connection_to_ai=aiod.connection_to_ai,
            type=aiod.type,
            logo_url=aiod.logo_url,
            same_as=aiod.same_as,
            founding_date=aiod.founding_date,
            dissolution_date=aiod.dissolution_date,
            legal_name=aiod.legal_name,
            alternate_name=aiod.alternate_name,
            address=aiod.address,
            telephone=aiod.telephone,
            members=members,
            departments=departments,
            parent_organization_id=aiod.parent_organization,
            subsidiary_organization_id=aiod.subsidiary_organization,
            business_categories=[
                OrmBusinessCategory.as_unique(session=session, category=category)
                for category in aiod.business_categories
            ],
            technical_categories=[
                OrmTechnicalCategory.as_unique(session=session, category=category)
                for category in aiod.technical_categories
            ],
            email_addresses=[
                OrmEmail.as_unique(session=session, email=email) for email in aiod.email_addresses
            ],
        )

    def orm_to_aiod(self, orm: OrmOrganization) -> AIoDOrganization:
        """
        Converting between organization representations:
        the database variant towards the AIoD schema.
        """
        return AIoDOrganization(
            identifier=orm.identifier,
            name=orm.name,
            description=orm.description,
            image_url=orm.image_url,
            connection_to_ai=orm.connection_to_ai,
            type=orm.type,
            logo_url=orm.logo_url,
            same_as=orm.same_as,
            founding_date=orm.founding_date,
            dissolution_date=orm.dissolution_date,
            legal_name=orm.legal_name,
            alternate_name=orm.alternate_name,
            address=orm.address,
            telephone=orm.telephone,
            members={member for member in orm.members},
            departments={department for department in orm.departments},
            parent_organization=orm.parent_organization_id,
            subsidiary_organization=orm.subsidiary_organization_id,
            email_addresses={e.email for e in orm.email_addresses},
            business_categories={c.category for c in orm.business_categories},
            technical_categories={c.category for c in orm.technical_categories},
        )
