"""
Converting between different dataset representations
"""
from converters.dataset_converter import _retrieve_related_objects_by_ids
from database.model.dataset import OrmDataset
from database.model.publication import OrmPublication
from sqlalchemy.orm import Session

from schemas import AIoDPublication


def orm_to_aiod(orm: OrmPublication) -> AIoDPublication:
    """
    Converting between publication representations: the database variant (OrmDataset) towards the
    AIoD schema.
    """
    return AIoDPublication(
        id=orm.id,
        doi=orm.doi,
        node=orm.node,
        node_specific_identifier=orm.node_specific_identifier,
        title=orm.title,
        url=orm.url,
        datasets=[d.id for d in orm.datasets],
    )


def aiod_to_orm(session: Session, aiod: AIoDPublication) -> OrmPublication:
    """
    Converting between publication representations: the AIoD schema towards the database variant
    """
    datasets = _retrieve_related_objects_by_ids(session, aiod.datasets, OrmDataset)
    return OrmPublication(
        doi=aiod.doi,
        node=aiod.node,
        node_specific_identifier=aiod.node_specific_identifier,
        title=aiod.title,
        url=aiod.url,
        datasets=datasets,
    )
