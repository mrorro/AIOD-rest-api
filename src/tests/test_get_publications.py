from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import PublicationDescription


def test_happy_path(client: TestClient, engine: Engine):
    publications = [
        PublicationDescription(
            title="title 1", doi="10.5281/zenodo.121", node="zenodo", node_specific_identifier="121"
        ),
        PublicationDescription(
            title="title 2", doi="10.5281/zenodo.122", node="zenodo", node_specific_identifier="122"
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
    assert {pub["title"] for pub in response_json} == {"title 1", "title 2"}
    assert {pub["doi"] for pub in response_json} == {"10.5281/zenodo.121", "10.5281/zenodo.122"}
    assert {pub["node"] for pub in response_json} == {"zenodo", "zenodo"}
    assert {pub["node_specific_identifier"] for pub in response_json} == {"121", "122"}
    assert {pub["id"] for pub in response_json} == {1, 2}
    for pub in response_json:
        assert len(pub) == 5
