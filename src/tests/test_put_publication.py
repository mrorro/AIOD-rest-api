import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import PublicationDescription


@pytest.mark.parametrize(
    "identifier,title,doi,node,node_specific_identifier",
    [
        (1, "NEW NAME", "doi1", "zenodo", "1"),
        (1, "pub1", "doi1", "zenodo", "new-id"),
        (1, "pub1", "doi1", "other_node", "3"),
        (3, "pub2", "doi1", "other_node", "3"),
    ],
)
def test_happy_path(
    client: TestClient,
    engine: Engine,
    identifier: int,
    title: str,
    doi: str,
    node: str,
    node_specific_identifier: str,
):
    _setup(engine)
    response = client.put(
        f"/publications/{identifier}",
        json={
            "title": title,
            "doi": doi,
            "node": node,
            "node_specific_identifier": node_specific_identifier,
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == title
    assert response_json["doi"] == doi
    assert response_json["node"] == node
    assert response_json["node_specific_identifier"] == node_specific_identifier
    assert response_json["id"] == identifier
    assert len(response_json) == 6


def test_non_existent(client: TestClient, engine: Engine):
    _setup(engine)

    response = client.put(
        "/publications/4",
        json={"title": "pub2", "doi": "doi2", "node": "zenodo", "node_specific_identifier": "2"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Publication '4' not found in the database."


def test_partial_update(client: TestClient, engine: Engine):
    _setup(engine)

    response = client.put("/publications/4", json={"title": "title", "doi": "doi"})
    # Partial update: node and node_specific_identifier omitted. This is not supported,
    # and should be a PATCH request if we supported it.

    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"] == [
        {
            "loc": ["body", "node_specific_identifier"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {"loc": ["body", "node"], "msg": "field required", "type": "value_error.missing"},
    ]


def test_too_long_name(client: TestClient, engine: Engine):
    _setup(engine)

    title = "a" * 200
    response = client.put(
        "/publications/4",
        json={"title": title, "doi": "doi2", "node": "node", "node_specific_identifier": "id"},
    )
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"] == [
        {
            "ctx": {"limit_value": 150},
            "loc": ["body", "title"],
            "msg": "ensure this value has at most 150 characters",
            "type": "value_error.any_str.max_length",
        }
    ]


def _setup(engine):
    datasets = [
        PublicationDescription(
            title="pub1", doi="doi1", node="zenodo", node_specific_identifier="1"
        ),
        PublicationDescription(
            title="pub1", doi="doi2", node="other", node_specific_identifier="1"
        ),
        PublicationDescription(
            title="pub2", doi="doi3", node="zenodo", node_specific_identifier="2"
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()
