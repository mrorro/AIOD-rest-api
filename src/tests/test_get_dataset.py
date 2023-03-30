import copy

from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.dataset import OrmDataset

OPENML_URL = "https://www.openml.org/api/v1/json"


def test_happy_path(client: TestClient, engine: Engine):
    dataset_description = OrmDataset(
        name="anneal",
        node="openml",
        description="description text",
        same_as="",
        node_specific_identifier="1",
    )
    with Session(engine) as session:
        # Populate database.
        # Deepcopy necessary because SqlAlchemy changes the instance so that accessing the
        # node_specific_identifier is not possible anymore
        session.add(copy.deepcopy(dataset_description))
        session.commit()
    response = client.get("/nodes/openml/datasets/1")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["name"] == "anneal"
    assert response_json["description"] == "description text"
    assert response_json["identifier"] == 1


def test_dataset_not_found_in_local_db(client: TestClient, engine: Engine):
    dataset_description = OrmDataset(
        name="anneal", node="openml", description="", same_as="", node_specific_identifier="1"
    )
    with Session(engine) as session:
        # Populate database
        session.add(dataset_description)
        session.commit()
    response = client.get("/nodes/openml/datasets/2")  # Note that only dataset 1 exists
    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset '2' of 'openml' not found in the database."


def test_wrong_node(client: TestClient, engine: Engine):
    dataset_description = OrmDataset(
        name="anneal", node="example", description="", same_as="", node_specific_identifier="1"
    )
    with Session(engine) as session:
        # Populate database
        session.add(dataset_description)
        session.commit()
    response = client.get("/nodes/openml/datasets/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset '1' of 'openml' not found in the database."


def test_unexisting_node(client: TestClient, engine: Engine):
    dataset_description = OrmDataset(
        name="anneal",
        node="openml",
        description="",
        same_as="",
        node_specific_identifier="1",
    )
    with Session(engine) as session:
        # Populate database
        session.add(dataset_description)
        session.commit()
    response = client.get("/nodes/unexisting_node/datasets/1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Node 'unexisting_node' not recognized."
