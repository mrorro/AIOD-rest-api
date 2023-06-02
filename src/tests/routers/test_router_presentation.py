"""
Dataset is a complex resource, so they are tested separately.
"""

import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from unittest.mock import Mock

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from authentication import keycloak_openid
from database.model import AIAsset
from database.model.presentation import Presentation


def test_happy_path(client: TestClient, engine: Engine, mocked_privileged_token: Mock):
    keycloak_openid.decode_token = mocked_privileged_token
    with Session(engine) as session:
        session.add_all(
            [
                AIAsset(type="presentation"),
                Presentation(
                    identifier="1",
                    name="Presentation",
                    description="description text",
                    platform="example",
                    platform_identifier="1",
                ),
            ]
        )
        session.commit()

    body = {
        "platform": "example",
        "platform_identifier": "3",
        "description": "description text",
        "name": "Example Presentation",
    }
    response = client.post("/presentations/v0", json=body, headers={"Authorization": "Fake token"})
    assert response.status_code == 200

    response = client.get("/presentations/v0/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["identifier"] == 2
    assert response_json["name"] == "Example Presentation"
    assert response_json["description"] == "description text"
    assert response_json["platform"] == "example"
    assert response_json["platform_identifier"] == "3"
