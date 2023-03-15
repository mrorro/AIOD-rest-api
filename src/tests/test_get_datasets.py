from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import DatasetDescription


def test_happy_path(client: TestClient, engine: Engine):
    datasets = [
        DatasetDescription(
            name="dset1",
            node="openml",
            description="a",
            same_as="openml.eu/1",
            node_specific_identifier="1",
        ),
        DatasetDescription(
            name="dset1",
            node="other_node",
            description="b",
            same_as="other_node.eu/1",
            node_specific_identifier="1",
        ),
        DatasetDescription(
            name="dset2",
            node="other_node",
            description="c",
            same_as="other_node.eu/2",
            node_specific_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    response = client.get("/datasets")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 3
    assert {ds["name"] for ds in response_json} == {"dset1", "dset2"}
    assert {ds["description"] for ds in response_json} == {"a", "b", "c"}
    assert {ds["node"] for ds in response_json} == {"openml", "other_node"}
    assert {ds["node_specific_identifier"] for ds in response_json} == {"1", "2"}
    assert {ds["id"] for ds in response_json} == {1, 2, 3}
    assert {ds["same_as"] for ds in response_json} == {
        "openml.eu/1",
        "other_node.eu/1",
        "other_node.eu/2",
    }
    for ds in response_json:
        assert len(ds) == 6
