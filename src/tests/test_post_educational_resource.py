import typing
from database.model.base import Language, TargetAudience  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from datetime import datetime


from database.model.educational_resource import EducationalResource


def test_happy_path(client: TestClient, engine: Engine):
    date_format = "%Y-%m-%d"
    educational_resources = [
        EducationalResource(
            title="str",
            date_modified=datetime.strptime("2023-03-21", date_format),
            body="str",
            website_url="str",
            educational_role="Student",
            educational_level="Advanced" ,
            educatonal_type="MOOC",
            interactivity_type="str",
            accessibility_api="str",
            accessibility_control="str",
            access_mode="str",
            access_restrictions="str",
            citation="str",
            version="str",
            field_prerequisites="str",
            short_summary="str",
            duration_minutes_and_hours="str",
            hours_per_week="1-3 hours (lower-paced)",
            country="Sweeden",
            is_accessible_for_free=True,
            duration_in_years=2,
            pace="Full-time",
            time_required=0
        ),    
        EducationalResource(
            title="str",
            date_modified=datetime.strptime("2023-03-21", date_format),
            body="str",
            website_url="str",
            educational_role="Student",
            educational_level="Advanced" ,
            educatonal_type="MOOC",
            interactivity_type="str",
            accessibility_api="str",
            accessibility_control="str",
            access_mode="str",
            access_restrictions="str",
            citation="str",
            version="str",
            field_prerequisites="str",
            short_summary="str",
            duration_minutes_and_hours="str",
            hours_per_week="1-3 hours (lower-paced)",
            country="Sweeden",
            is_accessible_for_free=True,
            duration_in_years=2,
            pace="Full-time",
            time_required=0
        )
       
    ]
    language = Language(language="International")
    audience = TargetAudience(audience="Working professionals")

    with Session(engine) as session:
        # Populate database
        # session.add_all(educational_resources)
        session.add(language)
        session.add(audience)
        session.commit()

    response = client.post(
        "/educational_resource",
        json={
            "title": "string",
            "body": "string",
            "website_url": "string",
            "date_modified": "2023-03-27T08:49:40.261Z",
            "educational_use": "string",
            "website_link": "string",
            "typical_age_range": "string",
            "interactivity_type": "string",
            "accessibility_api": "string",
            "accessibility_control": "string",
            "access_mode": "string",
            "access_mode_sufficient": "string",
            "access_restrictions": "string",
            "is_accessible_for_free": "true",
            "time_required": 0,
            "citation": "string",
            "version": "string",
            "credits": "true",
            "number_of_weeks": 0,
            "field_prerequisites": "string",
            "short_summary": "string",
            "duration_in_years": 0,
            "duration_minutes_and_hours": "Less than 1 hour",
            "hours_per_week": "1-3 hours (lower-paced)",
            "educational_role": "Student",
            "educational_level": "Basic",
            "educatonal_type": "Distance Learning",
            "country": "Sweeden",
            "pace": "Full-time",
            "languages": [
                "International"
            ],
            "target_audience": [
                "Working professionals"
            ]
          
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == "string"
    assert response_json["body"] == "string"
    assert response_json["accessibility_control"] == "string"
    assert response_json["id"] == 1
    print(len(response_json))




@pytest.mark.parametrize(
    "title",
    ["\"'é:?", "!@#$%^&*()`~", "Ω≈ç√∫˜µ≤≥÷", "田中さんにあげて下さい", " أي بعد, ", "𝑻𝒉𝒆 𝐪𝐮𝐢𝐜𝐤", "گچپژ"],
)
def test_unicode(client: TestClient, engine: Engine, title):
    language = Language(language="International")
    audience = TargetAudience(audience="Working professionals")

    with Session(engine) as session:
        session.add(language)
        session.add(audience)
        session.commit()

    response = client.post(
        "/educational_resource",
        json={
            "title": title,
           "body": "string",
            "website_url": "string",
            "date_modified": "2023-03-27T08:49:40.261Z",
            "educational_use": "string",
            "website_link": "string",
            "typical_age_range": "string",
            "interactivity_type": "string",
            "accessibility_api": "string",
            "accessibility_control": "string",
            "access_mode": "string",
            "access_mode_sufficient": "string",
            "access_restrictions": "string",
            "is_accessible_for_free": "true",
            "time_required": 0,
            "citation": "string",
            "version": "string",
            "credits": "true",
            "number_of_weeks": 0,
            "field_prerequisites": "string",
            "short_summary": "string",
            "duration_in_years": 0,
            "duration_minutes_and_hours": "Less than 1 hour",
            "hours_per_week": "1-3 hours (lower-paced)",
            "educational_role": "Student",
            "educational_level": "Basic",
            "educatonal_type": "Distance Learning",
            "country": "Sweeden",
            "pace": "Full-time",
            "languages": [
                "International"
            ],
            "target_audience": [
                "Working professionals"
            ]
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == title
@pytest.mark.parametrize(
    "field",
    [
        "title",
        "body",
        "educational_role",
        "educational_level",
        "educatonal_type",
    ],
)
def test_missing_value(client: TestClient, engine: Engine, field: str):
    data={
        "title": "string",
        "body": "string",
        "website_url": "string",
        "date_modified": "2023-03-27T08:49:40.261Z",
        "educational_use": "string",
        "website_link": "string",
        "typical_age_range": "string",
        "interactivity_type": "string",
        "accessibility_api": "string",
        "accessibility_control": "string",
        "access_mode": "string",
        "access_mode_sufficient": "string",
        "access_restrictions": "string",
        "is_accessible_for_free": "true",
        "time_required": 0,
        "citation": "string",
        "version": "string",
        "credits": "true",
        "number_of_weeks": 0,
        "field_prerequisites": "string",
        "short_summary": "string",
        "duration_in_years": 0,
        "duration_minutes_and_hours": "Less than 1 hour",
        "hours_per_week": "1-3 hours (lower-paced)",
        "educational_role": "Student",
        "educational_level": "Basic",
        "educatonal_type": "Distance Learning",
        "country": "Sweeden",
        "pace": "Full-time",
        "languages": [
            "International"
        ],
        "target_audience": [
            "Working professionals"
        ]
    }
    del data[field]
    response = client.post("/educational_resource", json=data)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["body", field], "msg": "field required", "type": "value_error.missing"}
    ]



@pytest.mark.parametrize(
    "field",
    [
        "title",
        "body",
        "educational_role",
        "educational_level",
        "educatonal_type",
    ],
)
def test_null_value(client: TestClient, engine: Engine, field: str):
    data={
        "title": "string",
        "body": "string",
        "website_url": "string",
        "date_modified": "2023-03-27T08:49:40.261Z",
        "educational_use": "string",
        "website_link": "string",
        "typical_age_range": "string",
        "interactivity_type": "string",
        "accessibility_api": "string",
        "accessibility_control": "string",
        "access_mode": "string",
        "access_mode_sufficient": "string",
        "access_restrictions": "string",
        "is_accessible_for_free": "true",
        "time_required": 0,
        "citation": "string",
        "version": "string",
        "credits": "true",
        "number_of_weeks": 0,
        "field_prerequisites": "string",
        "short_summary": "string",
        "duration_in_years": 0,
        "duration_minutes_and_hours": "Less than 1 hour",
        "hours_per_week": "1-3 hours (lower-paced)",
        "educational_role": "Student",
        "educational_level": "Basic",
        "educatonal_type": "Distance Learning",
        "country": "Sweeden",
        "pace": "Full-time",
        "languages": [
            "International"
        ],
        "target_audience": [
            "Working professionals"
        ]
    }
    data[field] = None
    response = client.post("/educational_resource", json=data)
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body", field],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed",
        }
    ]
