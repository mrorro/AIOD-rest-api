import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from unittest.mock import Mock

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from authentication import keycloak_openid
from database.model import AIAsset
from database.model.educational_resource import EducationalResource


def test_happy_path(client: TestClient, engine: Engine, mocked_privileged_token: Mock):
    keycloak_openid.decode_token = mocked_privileged_token
    with Session(engine) as session:
        session.add_all(
            [
                AIAsset(type="educational_resource"),
                EducationalResource(
                    identifier=1,
                    title="news title",
                    platform_identifier="1",
                    platform="example",
                    date_modified="2021-02-05T15:15:00.000Z",
                    body="body",
                    website_url="url",
                    educational_level="educational_level",
                    educational_type="educational_type",
                    pace="pace",
                ),
            ]
        )
        session.commit()

    body = {
        "platform": "zenodo",
        "platform_identifier": "1",
        "title": "Example News",
        "date_modified": "2022-01-01T15:15:00.000Z",
        "body": "Example news body",
        "website_url": "https://example.com/educational_resource/example/website",
        "educational_level": "Example educational level",
        "educational_type": "Example educational type",
        "pace": "Example pace",
        "interactivity_type": "Example interactivity type",
        "typical_age_range": "Example  typical age range",
        "accessibility_api": "Example accessibility api",
        "accessibility_control": "Example accessibility control",
        "access_mode": "Example access mode",
        "access_mode_sufficient": "Example access mode",
        "access_restrictions": "Example access restrictions",
        "citations": "Example citations",
        "version": "Example version",
        "number_of_weeks": 0,
        "field_prerequisites": "Example field prerequisites",
        "short_summary": "Example short summary",
        "duration_minutes_and_hours": "Example duration minutes and hours",
        "hours_per_week": "Example hours per week",
        "country": "Example country",
        "is_accessible_for_free": True,
        "credits": True,
        "duration_in_years": 0,
        "languages": ["language 1", "language 2"],
    }
    response = client.post(
        "/educational_resources/v0", json=body, headers={"Authorization": "Fake token"}
    )
    assert response.status_code == 200

    response = client.get("/educational_resources/v0/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["identifier"] == 2
    assert response_json["platform"] == "zenodo"
    assert response_json["title"] == "Example News"
    assert response_json["date_modified"] == "2022-01-01T15:15:00"
    assert response_json["body"] == "Example news body"
    assert (
        response_json["website_url"] == "https://example.com/educational_resource/example/website"
    )
    assert response_json["educational_level"] == "Example educational level"
    assert response_json["educational_type"] == "Example educational type"
    assert response_json["pace"] == "Example pace"
    assert response_json["interactivity_type"] == "Example interactivity type"
    assert response_json["typical_age_range"] == "Example  typical age range"
    assert response_json["accessibility_api"] == "Example accessibility api"
    assert response_json["accessibility_control"] == "Example accessibility control"
    assert response_json["access_mode"] == "Example access mode"
    assert response_json["access_mode_sufficient"] == "Example access mode"
    assert response_json["access_restrictions"] == "Example access restrictions"
    assert response_json["citations"] == "Example citations"
    assert response_json["version"] == "Example version"
    assert response_json["number_of_weeks"] == 0
    assert response_json["field_prerequisites"] == "Example field prerequisites"
    assert response_json["short_summary"] == "Example short summary"
    assert response_json["duration_minutes_and_hours"] == "Example duration minutes and hours"
    assert response_json["hours_per_week"] == "Example hours per week"
    assert response_json["country"] == "Example country"
    assert response_json["is_accessible_for_free"]
    assert response_json["credits"]
    assert response_json["duration_in_years"] == 0
    assert set(response_json["languages"]) == {"language 1", "language 2"}
