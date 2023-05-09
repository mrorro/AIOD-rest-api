import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.dataset import OrmDataset

from unittest.mock import Mock
from authentication import keycloak_openid


def get_default_user():

    default_user = {
        "name": "test-user",
        "realm_access": {
            "roles": [
                "default-roles-dev",
                "offline_access",
                "uma_authorization",
            ]
        },
    }
    return default_user


def test_happy_path(client: TestClient, engine: Engine):

    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    datasets = [
        OrmDataset(
            name="dset1",
            platform="openml",
            description="",
            same_as="non-existing-url/1",
            platform_identifier="1",
        ),
        OrmDataset(
            name="dset1",
            platform="other_platform",
            description="",
            same_as="non-existing-url/2",
            platform_identifier="1",
        ),
        OrmDataset(
            name="dset2",
            platform="other_platform",
            description="",
            same_as="non-existing-url/3",
            platform_identifier="2",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()
    response = client.post(
        "/datasets/v0",
        json={
            "name": "dset2",
            "platform": "openml",
            "description": "description",
            "sameAs": "openml.org/datasets/1",
            "platformIdentifier": "2",
        },
        headers={"Authorization": "fake-token"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "dset2"
    assert response_json["description"] == "description"
    assert response_json["sameAs"] == "openml.org/datasets/1"
    assert response_json["platform"] == "openml"
    assert response_json["platformIdentifier"] == "2"
    assert response_json["identifier"] == 4
    assert len(response_json) == 14


@pytest.mark.parametrize(
    "name",
    ["\"'é:?", "!@#$%^&*()`~", "Ω≈ç√∫˜µ≤≥÷", "田中さんにあげて下さい", " أي بعد, ", "𝑻𝒉𝒆 𝐪𝐮𝐢𝐜𝐤", "گچپژ"],
)
def test_unicode(client: TestClient, engine: Engine, name):
    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    response = client.post(
        "/datasets/v0",
        json={
            "name": name,
            "platform": "openml",
            "platformIdentifier": "2",
            "description": f"Description of {name}",
            "sameAs": "url",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == name


def test_duplicated_dataset(client: TestClient, engine: Engine):
    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    datasets = [
        OrmDataset(
            name="dset1",
            platform="openml",
            platform_identifier="1",
            same_as="url",
            description="bla",
        )
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()
    response = client.post(
        "/datasets/v0",
        json={
            "name": "dset1",
            "description": "description",
            "sameAs": "url",
            "platform": "openml",
            "platformIdentifier": "1",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 409
    assert (
        response.json()["detail"] == "There already exists a dataset with the same platform "
        "and name, with identifier=1."
    )


@pytest.mark.parametrize("field", ["name", "sameAs", "description"])
def test_missing_value(client: TestClient, engine: Engine, field: str):
    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    data = {
        "name": "Name",
        "platform": "openml",
        "platformIdentifier": "1",
        "sameAs": "url",
        "description": "description",
    }  # type: typing.Dict[str, typing.Any]
    del data[field]
    response = client.post("/datasets", json=data, headers={"Authorization": "fake-token"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["body", field], "msg": "field required", "type": "value_error.missing"}
    ]


@pytest.mark.parametrize("field", ["name", "platform", "sameAs", "description"])
def test_null_value(client: TestClient, engine: Engine, field: str):
    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    data = {
        "name": "Name",
        "platform": "openml",
        "platformIdentifier": "1",
        "sameAs": "url",
        "description": "description",
    }  # type: typing.Dict[str, typing.Any]
    data[field] = None
    response = client.post("/datasets", json=data, headers={"Authorization": "fake-token"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body", field],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed",
        }
    ]


def test_unauthorized_user(client: TestClient, engine: Engine):

    user = get_default_user()
    keycloak_openid.decode_token = Mock(return_value=user)

    datasets = [
        OrmDataset(
            name="dset1",
            platform="openml",
            description="",
            same_as="non-existing-url/1",
            platform_identifier="1",
        )
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    response = client.post(
        "/datasets",
        json={
            "name": "dset2",
            "platform": "openml",
            "description": "description",
            "same_as": "openml.org/datasets/1",
            "platform_identifier": "2",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 403
    response_json = response.json()
    assert response_json["detail"] == "You donot have permission to edit Aiod resources"


def test_unauthenticated_user(client: TestClient, engine: Engine):

    datasets = [
        OrmDataset(
            name="dset1",
            platform="openml",
            description="",
            same_as="non-existing-url/1",
            platform_identifier="1",
        )
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(datasets)
        session.commit()

    response = client.post(
        "/datasets",
        json={
            "name": "dset2",
            "platform": "openml",
            "description": "description",
            "same_as": "openml.org/datasets/1",
            "platform_identifier": "2",
        },
    )
    assert response.status_code == 401
    response_json = response.json()
    assert response_json["detail"] == "Not logged in"
