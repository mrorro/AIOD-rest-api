"""
Converting between different dataset representations
"""

from typing import List

from sqlalchemy.orm import Session

from converters.abstract_converter import ResourceConverter
from converters.conversion_helpers import retrieve_related_objects_by_ids
from database.model.dataset import OrmDataset, OrmDataDownload, OrmMeasuredValue, OrmAlternateName
from database.model.general import (
    OrmLicense,
    OrmKeyword,
)
from database.model.publication import OrmPublication
from schemas import AIoDDataset, AIoDDistribution, AIoDMeasurementValue


class DatasetConverter(ResourceConverter[AIoDDataset, OrmDataset]):
    def aiod_to_orm(self, session: Session, aiod: AIoDDataset) -> OrmDataset:
        """
        Converting between dataset representations: the AIoD schema towards the database variant (
        OrmDataset)
        """
        if isinstance(aiod.citations, List):
            # TODO(issue 7): retrieve OrmPublication from AIoDPublication
            citations = []
        else:
            citations = retrieve_related_objects_by_ids(session, aiod.citations, OrmPublication)
        has_parts = retrieve_related_objects_by_ids(session, aiod.has_parts, OrmDataset)
        is_part = retrieve_related_objects_by_ids(session, aiod.is_part, OrmDataset)

        orm = OrmDataset(
            description=aiod.description,
            name=aiod.name,
            node=aiod.node,
            node_specific_identifier=aiod.node_specific_identifier,
            same_as=aiod.same_as,
            creator=aiod.creator,
            date_modified=aiod.date_modified,
            date_published=aiod.date_published,
            funder=aiod.funder,
            is_accessible_for_free=aiod.is_accessible_for_free,
            issn=aiod.issn,
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
                    content_url=orm_distr.content_url,
                    content_size_kb=orm_distr.content_size_kb,
                    description=orm_distr.description,
                    name=orm_distr.name,
                    encoding_format=orm_distr.encoding_format,
                )
                for orm_distr in aiod.distributions
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
        orm.id = aiod.id
        return orm

    def orm_to_aiod(self, orm: OrmDataset) -> AIoDDataset:
        """
        Converting between dataset representations: the database variant (OrmDataset) towards the
        AIoD schema.
        """
        return AIoDDataset(
            id=orm.id,
            description=orm.description,
            name=orm.name,
            node=orm.node,
            node_specific_identifier=orm.node_specific_identifier,
            same_as=orm.same_as,
            creator=orm.creator,
            date_modified=orm.date_modified,
            date_published=orm.date_published,
            funder=orm.funder,
            is_accessible_for_free=orm.is_accessible_for_free,
            issn=orm.issn,
            size=orm.size,
            spatial_coverage=orm.spatial_coverage,
            temporal_coverage_from=orm.temporal_coverage_from,
            temporal_coverage_to=orm.temporal_coverage_to,
            version=orm.version,
            license=orm.license.name if orm.license is not None else None,
            has_parts=[part.id for part in orm.has_parts],
            is_part=[part.id for part in orm.is_part],
            alternate_names=[alias.name for alias in orm.alternate_names],
            citations=[citation.id for citation in orm.citations],
            distributions=[
                AIoDDistribution(
                    content_url=orm_distr.content_url,
                    content_size_kb=orm_distr.content_size_kb,
                    description=orm_distr.description,
                    name=orm_distr.name,
                    encoding_format=orm_distr.encoding_format,
                )
                for orm_distr in orm.distributions
            ],
            keywords=[keyword.name for keyword in orm.keywords],
            measured_values=[
                AIoDMeasurementValue(variable=mv.variable, technique=mv.technique)
                for mv in orm.measured_values
            ],
        )
