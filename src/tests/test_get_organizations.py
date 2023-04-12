from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.organization import OrmOrganization


def test_happy_path(client: TestClient, engine: Engine):
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
        OrmOrganization(
            platform="other_platform",
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
        session.add_all(organizations)
        session.commit()

    response = client.get("/organizations")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 3
    assert {ds["name"] for ds in response_json} == {"string", "string2", "string3"}
    assert {ds["description"] for ds in response_json} == {"string", "string2", "string3"}
    assert {ds["connection_to_ai"] for ds in response_json} == {"string", "string2", "string3"}
