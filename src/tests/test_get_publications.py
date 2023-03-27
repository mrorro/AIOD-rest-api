from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.model.publication import OrmPublication


def test_happy_path(client: TestClient, engine: Engine):
    publications = [
        OrmPublication(
            title="Title 1", doi="doi1", node="zenodo", node_specific_identifier="1"
        ),
        OrmPublication(
            title="Title 2", doi="doi2", node="zenodo", node_specific_identifier="2"
        ),
    ]
    with Session(engine) as session:
        # Populate database
        session.add_all(publications)
        session.commit()

    response = client.get("/publications")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2
    assert {pub["title"] for pub in response_json} == {"Title 1", "Title 2"}
    assert {pub["doi"] for pub in response_json} == {"doi1", "doi2"}
    assert {pub["node"] for pub in response_json} == {"zenodo", "zenodo"}
    assert {pub["node_specific_identifier"] for pub in response_json} == {"1", "2"}
    assert {pub["id"] for pub in response_json} == {1, 2}
    for pub in response_json:
        assert len(pub) == 5
