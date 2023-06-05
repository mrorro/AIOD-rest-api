from unittest.mock import Mock

from starlette.testclient import TestClient

from authentication import keycloak_openid


def test_happy_path(client: TestClient, mocked_privileged_token: Mock):
    keycloak_openid.decode_token = mocked_privileged_token
    body = {
        "platform": "zenodo",
        "platform_identifier": "1",
        "name": "Example Event",
        "description": "example descriprion",
        "registration_url": "https://example.com/event/example/registration",
        "location": "Example location Event",
        "start_date": "2022-01-01T15:15:00",
        "end_date": "2022-01-01T15:15:00",
        "duration": "Example duration Event",
        "status": "Example status Event",
        "attendance_mode": "Example attendance mode Event",
        "type": "Example type Event",
    }
    response = client.post("/events/v0", json=body, headers={"Authorization": "Fake token"})
    assert response.status_code == 200

    response = client.get("/events/v0/1")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["identifier"] == 1
    assert response_json["platform"] == "zenodo"
    assert response_json["platform_identifier"] == "1"
    assert response_json["name"] == "Example Event"
    assert response_json["description"] == "example descriprion"
    assert response_json["registration_url"] == "https://example.com/event/example/registration"
    assert response_json["location"] == "Example location Event"
    assert response_json["start_date"] == "2022-01-01T15:15:00"
    assert response_json["end_date"] == "2022-01-01T15:15:00"
    assert response_json["duration"] == "Example duration Event"
    assert response_json["status"] == "Example status Event"
    assert response_json["attendance_mode"] == "Example attendance mode Event"
    assert response_json["type"] == "Example type Event"
