import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.dataset import OrmDataset
from authentication import keycloak_openid


@pytest.mark.parametrize(
    "identifier,name,platform,platform_identifier,same_as,description",
    [
        (1, "NEW NAME", "openml", "1", "url1", "description"),
        (1, "dset1", "openml", "new-id", "url2", "description dset1"),
        (1, "dset1", "other_platform", "3", "url3", "description dset1"),
        (3, "DSET2", "other_platform", "3", "http://test.org/dataset/1", "description DSET2"),
    ],
)
def test_happy_path(
    client: TestClient,
    engine: Engine,
    identifier: int,
    name: str,
    platform: str,
    platform_identifier: str,
    same_as: str,
    description: str,
    mocked_previlege_token,
):

    keycloak_openid.decode_token = mocked_previlege_token

    _setup(engine)
    response = client.put(
        f"/datasets/v0/{identifier}",
        json={
            "name": name,
            "platform": platform,
            "platformIdentifier": platform_identifier,
            "sameAs": same_as,
            "description": description,
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == name
    assert response_json["platform"] == platform
    assert response_json["platformIdentifier"] == platform_identifier
    assert response_json["identifier"] == identifier
    assert response_json["sameAs"] == same_as
    assert response_json["description"] == description
    assert len(response_json) == 14


def test_non_existent(client: TestClient, engine: Engine, mocked_previlege_token):
    _setup(engine)

    keycloak_openid.decode_token = mocked_previlege_token

    response = client.put(
        "/datasets/v0/4",
        json={
            "name": "name",
            "platform": "platform",
            "description": "description",
            "sameAs": "url",
            "platformIdentifier": "id",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Dataset '4' not found in the database."


def test_partial_update(client: TestClient, engine: Engine, mocked_previlege_token):
    _setup(engine)

    keycloak_openid.decode_token = mocked_previlege_token

    response = client.put(
        "/datasets/v0/4", json={"name": "name"}, headers={"Authorization": "fake-token"}
    )
    # Partial update: platform and platform_identifier omitted. This is not supported,
    # and should be a PATCH request if we supported it.

    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"] == [
        {"loc": ["body", "description"], "msg": "field required", "type": "value_error.missing"},
        {"loc": ["body", "sameAs"], "msg": "field required", "type": "value_error.missing"},
    ]


def test_too_long_name(client: TestClient, engine: Engine, mocked_previlege_token):
    _setup(engine)

    keycloak_openid.decode_token = mocked_previlege_token

    name = "a" * 200
    response = client.put(
        "/datasets/v0/4",
        json={
            "name": name,
            "platform": "platform",
            "description": "description",
            "sameAs": "url",
            "platformIdentifier": "id",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"] == [
        {
            "ctx": {"limit_value": 150},
            "loc": ["body", "name"],
            "msg": "ensure this value has at most 150 characters",
            "type": "value_error.any_str.max_length",
        }
    ]


def test_unauthorized_user(client: TestClient, engine: Engine, mocked_token):
    _setup(engine)

    keycloak_openid.decode_token = mocked_token

    response = client.put(
        "/datasets/v0/1",
        json={
            "name": "name",
            "platform": "platform",
            "description": "description",
            "same_as": "url",
            "platform_identifier": "id",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 403
    response_json = response.json()
    assert response_json["detail"] == "You do not have permission to edit Aiod resources."


def test_unauthenticated_user(client: TestClient, engine: Engine):
    _setup(engine)

    response = client.put(
        "/datasets/v0/4",
        json={
            "name": "name",
            "platform": "platform",
            "description": "description",
            "same_as": "url",
            "platform_identifier": "id",
        },
    )
    assert response.status_code == 401
    response_json = response.json()
    assert response_json["detail"] == "Not logged in"


def _setup(engine):
    datasets = [
        OrmDataset(
            name="dset1",
            platform="openml",
            same_as="openml.org/1",
            description="",
            platform_identifier="1",
        ),
        OrmDataset(
            name="dset1",
            platform="other_platform",
            same_as="other.org/1",
            description="",
            platform_identifier="1",
        ),
        OrmDataset(
            name="dset2",
            platform="other_platform",
            same_as="other.org/2",
            description="",
            platform_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()
