from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from database.model.presentation import OrmPresentation


def test_happy_path(client: TestClient, engine: Engine):
    presentations = [
        OrmPresentation(name="name", platform="example", platform_identifier="1"),
        OrmPresentation(name="name2", platform="example", platform_identifier="2"),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(presentations)
        session.commit()

    response = client.get("/presentations/v0")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2
    assert {pre["name"] for pre in response_json} == {"name", "name2"}

    for pre in response_json:
        assert len(pre) == 5
