from sqlalchemy.future import Engine
from starlette.testclient import TestClient


def test_get_happy_path(client_test_resource: TestClient, engine_test_resource_filled: Engine):
    response = client_test_resource.get("/platforms/example/test_resources/v0/1")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["title"] == "A title"
    assert response_json["identifier"] == 1
    assert "deprecated" not in response.headers


def test_not_found(client_test_resource: TestClient, engine_test_resource_filled: Engine):
    response = client_test_resource.get("/platforms/example/test_resources/v0/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Test_resource '99' of 'example' not found in the database."


def test_wrong_platform(client_test_resource: TestClient, engine_test_resource_filled: Engine):
    response = client_test_resource.get("/platforms/openml/test_resources/v0/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Test_resource '1' of 'openml' not found in the database."


def test_nonexistent_platform(
    client_test_resource: TestClient, engine_test_resource_filled: Engine
):
    response = client_test_resource.get("/platforms/nonexistent_platform/test_resources/v0/1")
    assert response.status_code == 400
    assert response.json()["detail"] == "platform 'nonexistent_platform' not recognized."
