"""
Converting between different presentation representations
"""
from sqlalchemy.orm import Session

from converters.orm_converters.orm_converter import OrmConverter
from database.model.presentation import OrmPresentation
from schemas import AIoDPresentation


class PresentationConverter(OrmConverter[AIoDPresentation, OrmPresentation]):
    def aiod_to_orm(
        self, session: Session, aiod: AIoDPresentation, return_existing_if_present: bool = False
    ) -> OrmPresentation:
        """
        Converting between presentation representations: the AIoD schema towards the orm variant
        """

        return OrmPresentation.create_or_get(
            session=session,
            create=not return_existing_if_present,
            platform=aiod.platform,
            platform_identifier=aiod.platform_identifier,
            name=aiod.name,
            author=aiod.author,
            description=aiod.description,
            url=aiod.url,
            datePublished=aiod.datePublished,
            publisher=aiod.publisher,
            image=aiod.image,
            is_accessible_for_free=aiod.is_accessible_for_free,
        )

    def orm_to_aiod(self, orm: OrmPresentation) -> AIoDPresentation:
        """
        Converting between presentations representations: the database variant (OrmDataset) towards
        the AIoD schema.
        """
        return AIoDPresentation(
            identifier=orm.identifier,
            name=orm.name,
            platform=orm.platform,
            platform_identifier=orm.platform_identifier,
            author=orm.author,
            description=orm.description,
            url=orm.url,
            datePublished=orm.datePublished,
            publisher=orm.publisher,
            image=orm.image,
            is_accessible_for_free=orm.is_accessible_for_free,
        )
