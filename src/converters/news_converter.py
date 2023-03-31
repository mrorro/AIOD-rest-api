"""
Converting between different news representations
"""
from sqlalchemy.orm import Session

from converters.abstract_converter import ResourceConverter
from database.model.general import OrmKeyword, OrmBusinessCategory
from database.model.news import OrmMedia, OrmNews, OrmNewsCategory
from schemas import AIoDNews


class NewsConverter(ResourceConverter[AIoDNews, OrmNews]):
    def aiod_to_orm(
        self, session: Session, aiod: AIoDNews, return_existing_if_present: bool = False
    ) -> OrmNews:
        """
        Converting between news representations: the AIoD schema towards the database variant
        """
        return OrmNews.create(
            session=session,
            return_existing_if_present=return_existing_if_present,
            node=aiod.node,
            node_specific_identifier=aiod.node_specific_identifier,
            title=aiod.title,
            date_modified=aiod.date_modified,
            body=aiod.body,
            source=aiod.source,
            headline=aiod.headline,
            alternative_headline=aiod.alternative_headline,
            section=aiod.section,
            word_count=aiod.word_count,
            keywords=[
                OrmKeyword.as_unique(session=session, name=keyword) for keyword in aiod.keywords
            ]
            if aiod.keywords
            else [],
            business_categories=[
                OrmBusinessCategory.as_unique(session=session, category=category)
                for category in aiod.business_categories
            ]
            if aiod.business_categories
            else [],
            news_categories=[
                OrmNewsCategory.as_unique(session=session, category=category)
                for category in aiod.news_categories
            ]
            if aiod.news_categories
            else [],
            media=[OrmMedia.as_unique(session=session, name=name) for name in aiod.media]
            if aiod.media
            else [],
        )

    def orm_to_aiod(self, orm: OrmNews) -> AIoDNews:
        """
        Converting between news representations: the database variant towards the AIoD schema.
        """
        return AIoDNews(
            identifier=orm.identifier,
            node=orm.node,
            node_specific_identifier=orm.node_specific_identifier
            if orm.node_specific_identifier is not None
            else str(orm.identifier),
            title=orm.title,
            date_modified=orm.date_modified,
            body=orm.body,
            source=orm.source,
            headline=orm.headline,
            alternative_headline=orm.alternative_headline,
            section=orm.section,
            word_count=orm.word_count,
            keywords={k.name for k in orm.keywords},
            business_categories={c.category for c in orm.business_categories},
            news_categories={c.category for c in orm.news_categories},
            media={m.name for m in orm.media},
        )
