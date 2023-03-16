from typing import List, TypeVar, Type, Set

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    OrmDataset,
    OrmLicense,
    OrmAlternateName,
    OrmMeasuredValue,
    OrmKeyword,
    OrmPublication,
    Base,
)
from schemas import AIoDDataset, AIoDDistribution, AIoDMeasurementValue


def orm_to_aiod(orm: OrmDataset) -> AIoDDataset:
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


def aiod_to_orm(session: Session, aiod: AIoDDataset) -> OrmDataset:
    """
    Converting between dataset representations: the AIoD schema towards the database variant (
    OrmDataset)
    """

    citations = _retrieve_related_objects_by_ids(
        session, aiod.citations, OrmPublication
    )  # type: ignore
    has_parts = _retrieve_related_objects_by_ids(session, aiod.has_parts, OrmDataset)
    is_part = _retrieve_related_objects_by_ids(session, aiod.is_part, OrmDataset)

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
            AIoDDistribution(
                content_url=orm_distr.content_url,
                content_size_kb=orm_distr.content_size_kb,
                description=orm_distr.description,
                name=orm_distr.name,
                encoding_format=orm_distr.encoding_format,
            )
            for orm_distr in aiod.distributions
        ],
        keywords=[OrmKeyword.as_unique(session=session, name=keyword) for keyword in aiod.keywords],
        measured_values=[
            OrmMeasuredValue.as_unique(
                session=session, variable=mv.variable, technique=mv.technique
            )
            for mv in aiod.measured_values
        ],
    )
    orm.id = aiod.id
    return orm


T = TypeVar("T", bound=Base)


def _retrieve_related_objects_by_ids(
    session: Session, ids_or_objects: Set[str] | List[T], cls: Type[T]
) -> List[T]:
    if isinstance(ids_or_objects, List):
        related_objects: List[T] = ids_or_objects
        return related_objects
    ids: Set[str] = ids_or_objects
    related_objects = []
    if len(ids) > 0:
        query = select(cls).where(cls.id.in_(ids))
        related_objects = session.scalars(query).all()
        if len(related_objects) != len(ids):
            ids_not_found = set(ids) - {c.id for c in related_objects}
            raise HTTPException(
                status_code=404,
                detail=f"Dataset parts '{', '.join(ids_not_found)}' not found in the database.",
            )
    return related_objects
