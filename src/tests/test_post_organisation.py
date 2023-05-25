import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient


from database.model.organisation import OrmOrganisation
from platform_names import PlatformName

from authentication import keycloak_openid


def test_happy_path(client: TestClient, engine: Engine, mocked_privileged_token):

    keycloak_openid.decode_token = mocked_privileged_token

    organisations = [
        OrmOrganisation(
            platform=PlatformName.aiod,
            platform_identifier=None,
            name="string",
            description="string",
            connection_to_ai="string",
            type="string",
            image_url="string",
        ),
        OrmOrganisation(
            platform=PlatformName.aiod,
            platform_identifier=None,
            name="string2",
            description="string2",
            connection_to_ai="string2",
            type="string",
            image_url="string",
        ),
        OrmOrganisation(
            platform=PlatformName.aiod,
            platform_identifier=None,
            name="string3",
            description="string3",
            connection_to_ai="string3",
            type="string",
            image_url="string",
        ),
    ]

    with Session(engine) as session:
        # Populate database
        session.add_all(organisations)
        session.commit()

    response = client.post(
        "/organisations/v0",
        json={
            "platform": PlatformName.aiod,
            "platformIdentifier": None,
            "name": "string",
            "description": "string",
            "connection_to_ai": "string",
            "type": "string",
            "image_url": "string",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "string"
    assert response_json["description"] == "string"
    assert response_json["connectionToAi"] == "string"
    assert response_json["type"] == "string"
    assert response_json["identifier"] == 4


@pytest.mark.parametrize(
    "name",
    ["\"'é:?", "!@#$%^&*()`~", "Ω≈ç√∫˜µ≤≥÷", "田中さんにあげて下さい", " أي بعد, ", "𝑻𝒉𝒆 𝐪𝐮𝐢𝐜𝐤", "گچپژ"],
)
def test_unicode(client: TestClient, engine: Engine, name, mocked_privileged_token):

    keycloak_openid.decode_token = mocked_privileged_token

    response = client.post(
        "/organisations/v0",
        json={
            "platform": PlatformName.aiod,
            "platformIdentifier": None,
            "name": name,
            "description": "string",
            "connection_to_ai": "string",
            "type": "string",
            "image_url": "string",
        },
        headers={"Authorization": "fake-token"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == name


@pytest.mark.parametrize(
    "field",
    [
        "type",
    ],
)
def test_missing_value(client: TestClient, engine: Engine, field: str, mocked_privileged_token):

    keycloak_openid.decode_token = mocked_privileged_token

    data = {
        "platform": PlatformName.aiod,
        "platformIdentifier": None,
        "name": "string",
        "description": "string",
        "connectionToAi": "string",
        "type": "string",
        "imageUrl": "string",
    }  # type: typing.Dict[str, typing.Any]
    del data[field]
    response = client.post("/organisations/v0", json=data, headers={"Authorization": "fake-token"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["body", field], "msg": "field required", "type": "value_error.missing"}
    ]


@pytest.mark.parametrize(
    "field",
    [
        "type",
    ],
)
def test_null_value(client: TestClient, engine: Engine, field: str, mocked_privileged_token):

    keycloak_openid.decode_token = mocked_privileged_token

    data = {
        "platform": PlatformName.aiod,
        "platformIdentifier": None,
        "name": "string",
        "description": "string",
        "connection_to_ai": "string",
        "type": "string",
        "image_url": "string",
    }  # type: typing.Dict[str, typing.Any]
    data[field] = None
    response = client.post("/organisations/v0", json=data, headers={"Authorization": "fake-token"})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body", field],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed",
        }
    ]


def test_unauthorized_user(client: TestClient, engine: Engine, mocked_token):

    keycloak_openid.decode_token = mocked_token

    response = client.post(
        "/organisations/v0",
        json={
            "platform": PlatformName.aiod,
            "platformIdentifier": None,
            "name": "string",
            "description": "string",
            "connection_to_ai": "string",
            "type": "string",
            "image_url": "string",
        },
        headers={"Authorization": "fake-token"},
    )

    assert response.status_code == 403
    response_json = response.json()
    assert response_json["detail"] == "You do not have permission to edit Aiod resources."


def test_unauthenticated_user(client: TestClient, engine: Engine):

    response = client.post(
        "/organisations/v0",
        json={
            "platform": PlatformName.aiod,
            "platformIdentifier": None,
            "name": "string",
            "description": "string",
            "connection_to_ai": "string",
            "type": "string",
            "image_url": "string",
        },
    )

    assert response.status_code == 401
    response_json = response.json()
    assert (
        response_json["detail"] == "This endpoint requires authorization. You need to be logged in."
    )
