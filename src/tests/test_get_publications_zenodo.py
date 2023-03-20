from sqlalchemy import Engine
from starlette.testclient import TestClient


ZENODO_URL = "https://zenodo.org/api"


def test_happy_path(client: TestClient, engine: Engine):

    response = client.get("/nodes/zenodo/publications/")

    assert response.status_code == 501
