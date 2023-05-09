from sqlalchemy import Engine
from starlette.testclient import TestClient

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


def test_authorized(client: TestClient, engine: Engine):
    user = get_default_user()
    user["realm_access"]["roles"].append("edit_aiod_resources")
    keycloak_openid.decode_token = Mock(return_value=user)

    response = client.get("/authorization_test", headers={"Authorization": "fake-token"})
    assert response.status_code == 200


def test_unauthorized(client: TestClient, engine: Engine):
    user = get_default_user()
    keycloak_openid.decode_token = Mock(return_value=user)

    response = client.put(
        "/datasets/4",
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
    assert response_json["detail"] == "You donot have permission to edit Aiod resources"


def test_unauthenticated(client: TestClient, engine: Engine):
    response = client.get("/authorization_test")
    assert response.status_code == 401
    response_json = response.json()
    assert response_json["detail"] == "Not logged in"
