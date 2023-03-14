import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine, select, func
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import PublicationDescription


@pytest.mark.parametrize("identifier", ["1", "2"])
def test_happy_path(client: TestClient, engine: Engine, identifier: str):
    publications = [
        PublicationDescription(
            title="title 1",
            doi="10.5281/zenodo.121",
            node="zenodo",
            node_specific_identifier="121",
            datasets=[],
        ),
        PublicationDescription(
            title="title 2",
            doi="10.5281/zenodo.122",
            node="zenodo",
            node_specific_identifier="122",
            datasets=[],
        ),
    ]

    with Session(engine) as session:
        # Populate database
        session.add_all(publications)
        session.commit()

    assert _n_datasets(engine) == 2
    response = client.delete(f"/publications/{identifier}")
    assert response.status_code == 200
    assert _n_datasets(engine) == 1


@pytest.mark.parametrize("identifier", ["4", "5"])
def test_nonexistent_dataset(client: TestClient, engine: Engine, identifier: str):
    publications = [
        PublicationDescription(
            title="title 1",
            doi="10.5281/zenodo.121",
            node="zenodo",
            node_specific_identifier="121",
            datasets=[],
        ),
        PublicationDescription(
            title="title 2",
            doi="10.5281/zenodo.122",
            node="zenodo",
            node_specific_identifier="122",
            datasets=[],
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(publications)
        session.commit()

    assert _n_datasets(engine) == 2
    response = client.delete(f"/publications/{identifier}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Publication '{identifier}' not found in the database."
    assert _n_datasets(engine) == 2


def _n_datasets(engine: Engine) -> int:
    with Session(engine) as session:
        statement = select(func.count()).select_from(PublicationDescription)
        return session.execute(statement).scalar()
