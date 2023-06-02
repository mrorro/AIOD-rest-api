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
from database.model.news import News


def test_happy_path(client: TestClient, engine: Engine, mocked_privileged_token: Mock):
    keycloak_openid.decode_token = mocked_privileged_token
    with Session(engine) as session:
        session.add_all(
            [
                AIAsset(type="news"),
                News(
                    identifier=1,
                    title="news title",
                    platform_identifier="1",
                    platform="example",
                    date_modified="2021-02-05T15:15:00.000Z",
                    body="body",
                    section="example section",
                    word_count=100,
                    headline="example headline",
                ),
            ]
        )
        session.commit()

    body = {
        "platform": "example",
        "platform_identifier": "2",
        "title": "Example News",
        "date_modified": "2022-01-01T15:15:00.000Z",
        "body": "Example news body",
        "section": "Example news section",
        "headline": "Example news headline",
        "word_count": 100,
        "source": "https://news.source.example",
        "alternative_headline": "Example news alternative headline",
    }
    response = client.post("/news/v0", json=body, headers={"Authorization": "Fake token"})
    assert response.status_code == 200

    response = client.get("/news/v0/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["identifier"] == 2
    assert response_json["platform"] == "example"
    assert response_json["platform_identifier"] == "2"
    assert response_json["title"] == "Example News"
    assert response_json["date_modified"] == "2022-01-01T15:15:00"
    assert response_json["body"] == "Example news body"
    assert response_json["section"] == "Example news section"
    assert response_json["headline"] == "Example news headline"
    assert response_json["section"] == "Example news section"
    assert response_json["word_count"] == 100
    assert response_json["source"] == "https://news.source.example"
    assert response_json["alternative_headline"] == "Example news alternative headline"
