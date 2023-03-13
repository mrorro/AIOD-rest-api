import copy

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import PublicationDescription, DatasetDescription


@pytest.mark.parametrize("publication_id", [1, 2])
def test_happy_path(client: TestClient, engine: Engine, publication_id: int):
    datasets = [
        DatasetDescription(name="dset1", node="zenodo", node_specific_identifier="1"),
        DatasetDescription(name="dset1", node="other_node", node_specific_identifier="1"),
    ]
    publications = [
        PublicationDescription(
            doi="10.5281/zenodo.121",
            node="zenodo",
            node_specific_identifier="121",
            datasets=datasets,
        ),
        PublicationDescription(
            doi="10.5281/zenodo.122",
            node="zenodo",
            node_specific_identifier="122",
            datasets=datasets,
        ),
    ]
    with Session(engine) as session:
        # Populate database
        # Deepcopy necessary because SqlAlchemy changes the instance so that accessing the
        # attributes is not possible anymore
        session.add_all(copy.deepcopy(publications))
        session.commit()

    response = client.get(f"/publications/{publication_id}")
    assert response.status_code == 200
    response_json = response.json()

    expected = publications[publication_id - 1]
    assert response_json["doi"] == expected.doi
    assert response_json["node"] == expected.node
    assert response_json["node_specific_identifier"] == expected.node_specific_identifier
    assert response_json["id"] == publication_id
    assert len(response_json["datasets"]) == len(datasets)
    assert len(response_json) == 5


@pytest.mark.parametrize("publication_id", [-1, 2, 3])
def test_empty_db(client: TestClient, engine: Engine, publication_id):
    response = client.get(f"/publications/{publication_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Publication '{publication_id}' not found in the database."
    


@pytest.mark.parametrize("publication_id", [-1, 2, 3])
def test_publication_not_found(client: TestClient, engine: Engine, publication_id):
    publications = [
        PublicationDescription(
            doi="10.5281/zenodo.121", node="zenodo", node_specific_identifier="121", datasets=[]
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(publications)
        session.commit()
    response = client.get(f"/publications/{publication_id}")  # Note that only publication 1 exists
    assert response.status_code == 404
    assert response.json()["detail"] ==  f"Publication '{publication_id}' not found in the database."
    