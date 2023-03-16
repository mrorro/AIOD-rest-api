from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from connectors import (
    ExampleDatasetConnector,
    ExamplePublicationConnector,
)
from database.models import OrmPublication, OrmDataset
from database.setup import populate_database

OPENML_URL = "https://www.openml.org/api/v1/json"
HUGGINGFACE_URL = "https://datasets-server.huggingface.co"


def test_example_happy_path(engine: Engine):
    populate_database(
        engine,
        dataset_connectors=[ExampleDatasetConnector()],
        publications_connectors=[ExamplePublicationConnector()],
    )
    with Session(engine) as session:
        datasets = session.scalars(select(OrmDataset)).all()
        publications = session.scalars(select(OrmPublication)).all()
        assert len(datasets) == 5
        assert len(publications) == 2
        assert {len(d.citations) for d in datasets} == {0, 1, 2}
        assert {len(p.datasets) for p in publications} == {1, 2}
