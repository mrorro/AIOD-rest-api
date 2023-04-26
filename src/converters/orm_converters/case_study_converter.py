"""
Converting between different CaseStudy representations
"""

from sqlalchemy.orm import Session

from converters.orm_converters.orm_converter import OrmConverter, datetime_or_date
from database.model.case_study import OrmCaseStudy
from database.model.dataset import (
    OrmAlternateName,
)
from database.model.general import (
    OrmKeyword,
    OrmBusinessCategory,
    OrmTechnicalCategory,
)
from schemas import AIoDCaseStudy


class CaseStudyConverter(OrmConverter[AIoDCaseStudy, OrmCaseStudy]):
    def aiod_to_orm(
        self, session: Session, aiod: AIoDCaseStudy, return_existing_if_present: bool = False
    ) -> OrmCaseStudy:
        """
        Converting between case study representations: the AIoD schema towards the database
        variant
        """
        orm = OrmCaseStudy.create_or_get(
            create=not return_existing_if_present,
            session=session,
            description=aiod.description,
            name=aiod.name,
            platform=aiod.platform,
            platform_identifier=aiod.platform_identifier,
            same_as=aiod.same_as,
            creator=aiod.creator,
            date_modified=aiod.date_modified,
            date_published=aiod.date_published,
            is_accessible_for_free=aiod.is_accessible_for_free,
            publisher=aiod.publisher,
            alternate_names=[
                OrmAlternateName.as_unique(session=session, name=alias)
                for alias in aiod.alternate_names
            ],
            business_categories=[
                OrmBusinessCategory.as_unique(session=session, name=name)
                for name in aiod.business_categories
            ],
            keywords=[
                OrmKeyword.as_unique(session=session, name=keyword) for keyword in aiod.keywords
            ],
            technical_categories=[
                OrmTechnicalCategory.as_unique(session=session, name=name)
                for name in aiod.technical_categories
            ],
        )
        return orm

    def orm_to_aiod(self, orm: OrmCaseStudy) -> AIoDCaseStudy:
        """
        Converting between CaseStudy representations: the database variant towards the AIoD schema.
        """
        return AIoDCaseStudy(
            identifier=orm.identifier,
            description=orm.description,
            name=orm.name,
            platform=orm.platform,
            platform_identifier=orm.platform_identifier,
            same_as=orm.same_as,
            creator=orm.creator,
            date_modified=datetime_or_date(orm.date_modified),
            date_published=datetime_or_date(orm.date_published),
            is_accessible_for_free=orm.is_accessible_for_free,
            publisher=orm.publisher,
            alternate_names=[alias.name for alias in orm.alternate_names],
            business_categories=[category.name for category in orm.business_categories],
            keywords=[keyword.name for keyword in orm.keywords],
            technical_categories=[category.name for category in orm.technical_categories],
        )
