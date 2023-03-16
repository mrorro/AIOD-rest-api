import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine, select, func
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.dataset import OrmDataset


@pytest.mark.parametrize("identifier", ["1", "2", "3"])
def test_happy_path(client: TestClient, engine: Engine, identifier: str):
    datasets = [
        OrmDataset(
            name="dset1",
            description="",
            node="openml",
            same_as="url_openml",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset1",
            description="",
            node="other_node",
            same_as="url_other_node_1",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset2",
            description="",
            node="other_node",
            same_as="url_other_node_2",
            node_specific_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    assert _n_datasets(engine) == 3
    response = client.delete(f"/datasets/{identifier}")
    assert response.status_code == 200
    assert _n_datasets(engine) == 2


@pytest.mark.parametrize("identifier", ["4", "5"])
def test_nonexistent_dataset(client: TestClient, engine: Engine, identifier: str):
    datasets = [
        OrmDataset(
            name="dset1",
            node="openml",
            description="",
            same_as="openml.eu/1",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset1",
            node="other_node",
            description="",
            same_as="other_node.eu/1",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset2",
            node="other_node",
            description="",
            same_as="other_node.eu/2",
            node_specific_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    assert _n_datasets(engine) == 3
    response = client.delete(f"/datasets/{identifier}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Dataset '{identifier}' not found in the database."
    assert _n_datasets(engine) == 3


def _n_datasets(engine: Engine) -> int:
    with Session(engine) as session:
        statement = select(func.count()).select_from(OrmDataset)
        return session.execute(statement).scalar()
