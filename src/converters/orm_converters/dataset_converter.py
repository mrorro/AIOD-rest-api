"""
Converting between different dataset representations
"""

from sqlalchemy.orm import Session

from converters.orm_converters.abstract_converter import OrmConverter
from converters.orm_converters.conversion_helpers import retrieve_related_objects_by_ids
from database.model.dataset import (
    OrmDataset,
    OrmDataDownload,
    OrmMeasuredValue,
    OrmAlternateName,
    OrmChecksum,
    OrmChecksumAlgorithm,
)
from database.model.general import (
    OrmLicense,
    OrmKeyword,
)
from database.model.publication import OrmPublication
from schemas import AIoDDataset, AIoDDistribution, AIoDMeasurementValue, AIoDChecksum


class DatasetConverter(OrmConverter[AIoDDataset, OrmDataset]):
    def aiod_to_orm(
        self, session: Session, aiod: AIoDDataset, return_existing_if_present: bool = False
    ) -> OrmDataset:
        """
        Converting between dataset representations: the AIoD schema towards the database variant (
        OrmDataset)
        """
        citations = retrieve_related_objects_by_ids(session, aiod.citations, OrmPublication)
        has_parts = retrieve_related_objects_by_ids(session, aiod.has_parts, OrmDataset)
        is_part = retrieve_related_objects_by_ids(session, aiod.is_part, OrmDataset)

        orm = OrmDataset.create_or_get(
            create=not return_existing_if_present,
            session=session,
            description=aiod.description,
            name=aiod.name,
            platform=aiod.platform,
            platform_identifier=aiod.platform_identifier,
            same_as=aiod.same_as,
            contact=aiod.contact,
            creator=aiod.creator,
            date_modified=aiod.date_modified,
            date_published=aiod.date_published,
            funder=aiod.funder,
            is_accessible_for_free=aiod.is_accessible_for_free,
            issn=aiod.issn,
            publisher=aiod.publisher,
            size=aiod.size,
            spatial_coverage=aiod.spatial_coverage,
            temporal_coverage_from=aiod.temporal_coverage_from,
            temporal_coverage_to=aiod.temporal_coverage_to,
            version=aiod.version,
            license=OrmLicense.as_unique(session=session, name=aiod.license)
            if aiod.license is not None
            else None,
            has_parts=has_parts,
            is_part=is_part,
            alternate_names=[
                OrmAlternateName.as_unique(session=session, name=alias)
                for alias in aiod.alternate_names
            ],
            citations=citations,
            distributions=[
                OrmDataDownload(
                    content_url=distr.content_url,
                    content_size_kb=distr.content_size_kb,
                    description=distr.description,
                    name=distr.name,
                    encoding_format=distr.encoding_format,
                    checksum=[
                        OrmChecksum(
                            algorithm=OrmChecksumAlgorithm.as_unique(
                                session=session, name=checksum.algorithm
                            ),
                            value=checksum.value,
                        )
                        for checksum in distr.checksum
                    ],
                )
                for distr in aiod.distributions
            ],
            keywords=[
                OrmKeyword.as_unique(session=session, name=keyword) for keyword in aiod.keywords
            ],
            measured_values=[
                OrmMeasuredValue.as_unique(
                    session=session, variable=mv.variable, technique=mv.technique
                )
                for mv in aiod.measured_values
            ],
        )
        return orm

    def orm_to_aiod(self, orm: OrmDataset) -> AIoDDataset:
        """
        Converting between dataset representations: the database variant (OrmDataset) towards the
        AIoD schema.
        """
        return AIoDDataset(
            identifier=orm.identifier,
            description=orm.description,
            name=orm.name,
            platform=orm.platform,
            platform_identifier=orm.platform_identifier,
            same_as=orm.same_as,
            creator=orm.creator,
            date_modified=orm.date_modified,
            date_published=orm.date_published,
            funder=orm.funder,
            is_accessible_for_free=orm.is_accessible_for_free,
            issn=orm.issn,
            publisher=orm.publisher,
            size=orm.size,
            spatial_coverage=orm.spatial_coverage,
            temporal_coverage_from=orm.temporal_coverage_from,
            temporal_coverage_to=orm.temporal_coverage_to,
            version=orm.version,
            license=orm.license.name if orm.license is not None else None,
            has_parts=[part.identifier for part in orm.has_parts],
            is_part=[part.identifier for part in orm.is_part],
            alternate_names=[alias.name for alias in orm.alternate_names],
            citations=[citation.identifier for citation in orm.citations],
            distributions=[
                AIoDDistribution(
                    content_url=orm_distr.content_url,
                    content_size_kb=orm_distr.content_size_kb,
                    description=orm_distr.description,
                    name=orm_distr.name,
                    encoding_format=orm_distr.encoding_format,
                    checksum=[
                        AIoDChecksum(algorithm=checksum.algorithm.name, value=checksum.value)
                        for checksum in orm_distr.checksum
                    ],
                )
                for orm_distr in orm.distributions
            ],
            keywords=[keyword.name for keyword in orm.keywords],
            measured_values=[
                AIoDMeasurementValue(variable=mv.variable, technique=mv.technique)
                for mv in orm.measured_values
            ],
        )
