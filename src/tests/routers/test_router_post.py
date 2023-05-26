import pytest
from starlette.testclient import TestClient


@pytest.mark.parametrize(
    "title",
    ["\"'é:?", "!@#$%^&*()`~", "Ω≈ç√∫˜µ≤≥÷", "田中さんにあげて下さい", " أي بعد, ", "𝑻𝒉𝒆 𝐪𝐮𝐢𝐜𝐤", "گچپژ"],
)
def test_unicode(client_test_resource: TestClient, title: str):
    response = client_test_resource.post(
        "/test_resources/v0",
        json={"title": title, "platform": "example", "platform_identifier": "1"},
    )
    assert response.status_code == 200
    assert response.json() == {"identifier": 1}
    response = client_test_resource.get("/test_resources/v0/1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == title


def test_duplicated_resource(client_test_resource: TestClient):
    body = {"title": "title", "platform": "example", "platform_identifier": "1"}
    response = client_test_resource.post("/test_resources/v0", json=body)
    assert response.status_code == 200
    response = client_test_resource.post("/test_resources/v0", json=body)
    assert response.status_code == 409
    assert (
        response.json()["detail"] == "There already exists a test_resource with the same platform "
        "and name, with identifier=1."
    )


def test_missing_value(client_test_resource: TestClient):
    body = {"platform": "example", "platform_identifier": "1"}
    response = client_test_resource.post("/test_resources/v0", json=body)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["body", "title"], "msg": "field required", "type": "value_error.missing"}
    ]


def test_null_value(client_test_resource: TestClient):
    body = {"title": None, "platform": "example", "platform_identifier": "1"}
    response = client_test_resource.post("/test_resources/v0", json=body)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body", "title"],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed",
        }
    ]
