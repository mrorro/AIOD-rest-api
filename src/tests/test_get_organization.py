import copy

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.organization import OrmOrganization


@pytest.mark.parametrize("organization_id", [1, 2])
def test_happy_path(client: TestClient, engine: Engine, organization_id: int):
    organizations = [
        OrmOrganization(
            platform="aiod",
            platform_identifier=None,
            name="string",
            description="string",
            connection_to_ai="string",
            type="string",
            image_url="string",
        ),
        OrmOrganization(
            platform="openml",
            platform_identifier=None,
            name="string2",
            description="string2",
            connection_to_ai="string2",
            type="string",
            image_url="string",
        ),
    ]
    with Session(engine) as session:
        # Populate database
        # Deepcopy necessary because SqlAlchemy changes the instance so that accessing the
        # attributes is not possible anymore
        session.add_all(copy.deepcopy(organizations))
        session.commit()

    response = client.get(f"/organizations/{organization_id}")
    assert response.status_code == 200
    response_json = response.json()

    expected = organizations[organization_id - 1]

    assert response_json["name"] == expected.name
    assert response_json["description"] == expected.description
    assert response_json["type"] == expected.type
    assert response_json["image_url"] == expected.image_url


@pytest.mark.parametrize("organization_id", [-1, 2, 3])
def test_empty_db(client: TestClient, engine: Engine, organization_id):
    response = client.get(f"/organizations/{organization_id}")
    assert response.status_code == 404
    assert (
        response.json()["detail"] == f"Organization '{organization_id}' not found in the database."
    )


@pytest.mark.parametrize("organization_id", [-1, 2, 3])
def test_organization_not_found(client: TestClient, engine: Engine, organization_id):
    organizations = [
        OrmOrganization(
            platform="aiod",
            platform_identifier=None,
            name="string",
            description="string",
            connection_to_ai="string",
            type="string",
            image_url="string",
        )
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(organizations)
        session.commit()
    response = client.get(f"/organizations/{organization_id}")
    assert response.status_code == 404
    assert (
        response.json()["detail"] == f"Organization '{organization_id}' not found in the database."
    )
