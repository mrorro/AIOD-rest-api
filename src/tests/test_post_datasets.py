import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.dataset import OrmDataset


def test_happy_path(client: TestClient, engine: Engine):
    datasets = [
        OrmDataset(
            name="dset1",
            node="openml",
            description="",
            same_as="non-existing-url/1",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset1",
            node="other_node",
            description="",
            same_as="non-existing-url/2",
            node_specific_identifier="1",
        ),
        OrmDataset(
            name="dset2",
            node="other_node",
            description="",
            same_as="non-existing-url/3",
            node_specific_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    response = client.post(
        "/datasets",
        json={
            "name": "dset2",
            "node": "openml",
            "description": "description",
            "same_as": "openml.org/datasets/1",
            "node_specific_identifier": "2",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "dset2"
    assert response_json["description"] == "description"
    assert response_json["same_as"] == "openml.org/datasets/1"
    assert response_json["node"] == "openml"
    assert response_json["node_specific_identifier"] == "2"
    assert response_json["identifier"] == 4
    assert len(response_json) == 13


@pytest.mark.parametrize(
    "name",
    ["\"'é:?", "!@#$%^&*()`~", "Ω≈ç√∫˜µ≤≥÷", "田中さんにあげて下さい", " أي بعد, ", "𝑻𝒉𝒆 𝐪𝐮𝐢𝐜𝐤", "گچپژ"],
)
def test_unicode(client: TestClient, engine: Engine, name):
    response = client.post(
        "/datasets",
        json={
            "name": name,
            "node": "openml",
            "node_specific_identifier": "2",
            "description": f"Description of {name}",
            "same_as": "url",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == name


def test_duplicated_dataset(client: TestClient, engine: Engine):
    datasets = [
        OrmDataset(
            name="dset1",
            node="openml",
            node_specific_identifier="1",
            same_as="url",
            description="bla",
        )
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()
    response = client.post(
        "/datasets",
        json={
            "name": "dset1",
            "description": "description",
            "same_as": "url",
            "node": "openml",
            "node_specific_identifier": "1",
        },
    )
    assert response.status_code == 409
    assert (
        response.json()["detail"] == "There already exists a dataset with the same node "
        "and name, with identifier=1."
    )


@pytest.mark.parametrize("field", ["name", "same_as", "description"])
def test_missing_value(client: TestClient, engine: Engine, field: str):
    data = {
        "name": "Name",
        "node": "openml",
        "node_specific_identifier": "1",
        "same_as": "url",
        "description": "description",
    }  # type: typing.Dict[str, typing.Any]
    del data[field]
    response = client.post("/datasets", json=data)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["body", field], "msg": "field required", "type": "value_error.missing"}
    ]


@pytest.mark.parametrize("field", ["name", "node", "same_as", "description"])
def test_null_value(client: TestClient, engine: Engine, field: str):
    data = {
        "name": "Name",
        "node": "openml",
        "node_specific_identifier": "1",
        "same_as": "url",
        "description": "description",
    }  # type: typing.Dict[str, typing.Any]
    data[field] = None
    response = client.post("/datasets", json=data)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body", field],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed",
        }
    ]
