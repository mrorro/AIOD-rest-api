"""
Converting between different educational resource representations
"""
from ast import keyword
from sqlalchemy.orm import Session

from converters.abstract_converter import AbstractConverter
from database.model.general import OrmKeyword, OrmBusinessCategory, OrmTechnicalCategory
from database.model.educational_resource import OrmEducationalResource, OrmLanguage, OrmTargetAudience
from schemas import AIoDEducationalResource


class EducationalResourceConverter(AbstractConverter[AIoDEducationalResource, OrmEducationalResource]):
    def aiod_to_orm(self, session: Session, aiod: AIoDEducationalResource) -> OrmEducationalResource:
        """
        Converting between news representations: the AIoD schema towards the database variant
        """
        return OrmEducationalResource(
            title=aiod.title,
            date_modified=aiod.date_modified,
            body=aiod.body,
            website_url=aiod.website_url,
            educational_role=aiod.educational_role,
            educational_level=aiod.educational_level,
            educational_type=aiod.educational_type,
            interactivity_type=aiod.interactivity_type,
            accessibility_api=aiod.accessibility_api,
            accessibility_control=aiod.accessibility_control,
            access_mode=aiod.access_mode,
            access_mode_sufficient=aiod.access_mode_sufficient,
            access_restrictions=aiod.access_restrictions,
            citation=aiod.citation,
            typical_age_range=aiod.typical_age_range,
            version=aiod.version,
            number_of_weeks=aiod.number_of_weeks,
            credits=aiod.credits,
            field_prerequisites=aiod.field_prerequisites,
            short_summary=aiod.short_summary,
            duration_minutes_and_hours=aiod.duration_minutes_and_hours,
            hours_per_week=aiod.hours_per_week,
            country=aiod.country,
            is_accessible_for_free=aiod.is_accessible_for_free,
            duration_in_years=aiod.duration_in_years,
            pace=aiod.pace,
            time_required=aiod.time_required,
            keywords=[
                OrmKeyword.as_unique(session=session, name=keyword) for keyword in aiod.keywords
            ]
            if aiod.keywords
            else [],
            business_categories=[
                OrmBusinessCategory.as_unique(session=session, category=category) for category in aiod.business_categories
            ]
            if aiod.business_categories
            else [],
            technical_categories=[
                OrmTechnicalCategory.as_unique(session=session, category=category) for category in aiod.technical_categories
            ]
            if aiod.technical_categories
            else [],
            target_audience=[
                OrmTargetAudience.as_unique(session=session, name=name) for name in aiod.target_audience
            ]
            if aiod.target_audience
            else [],
            languages=[
                OrmLanguage.as_unique(session=session, name=name) for name in aiod.languages
            ]
            if aiod.languages
            else []
        
        
        )

    def orm_to_aiod(self, orm: OrmEducationalResource) -> AIoDEducationalResource:
        """
        Converting between news representations: the database variant towards the AIoD schema.
        """
        return AIoDEducationalResource(
            title=orm.title,
            date_modified=orm.date_modified,
            body=orm.body,
            website_url=orm.website_url,
            educational_role=orm.educational_role,
            educational_level=orm.educational_level,
            educational_type=orm.educational_type,
            interactivity_type=orm.interactivity_type,
            accessibility_api=orm.accessibility_api,
            accessibility_control=orm.accessibility_control,
            access_mode=orm.access_mode,
            access_mode_sufficient=orm.access_mode_sufficient,
            access_restrictions=orm.access_restrictions,
            citation=orm.citation,
            typical_age_range=orm.typical_age_range,
            version=orm.version,
            number_of_weeks=orm.number_of_weeks,
            credits=orm.credits,
            field_prerequisites=orm.field_prerequisites,
            short_summary=orm.short_summary,
            duration_minutes_and_hours=orm.duration_minutes_and_hours,
            hours_per_week=orm.hours_per_week,
            country=orm.country,
            is_accessible_for_free=orm.is_accessible_for_free,
            duration_in_years=orm.duration_in_years,
            pace=orm.pace,
            time_required=orm.time_required,
            business_categories={c.category for c in orm.business_categories},
            technical_categories={c.category for c in orm.technical_categories},
            keywords={k.name for k in orm.keywords},
            target_audience={t.name for t in orm.target_audience},
            languages={l.name for l in orm.languages},


        )
