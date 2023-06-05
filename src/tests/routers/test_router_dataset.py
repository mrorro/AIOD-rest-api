"""
Dataset is a complex resource, so they are tested separately.
"""

from unittest.mock import Mock

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from authentication import keycloak_openid
from database.model import AIAsset
from database.model.dataset.dataset import Dataset
from database.model.publication.publication import Publication


def test_happy_path(client: TestClient, engine: Engine, mocked_privileged_token: Mock):
    keycloak_openid.decode_token = mocked_privileged_token
    with Session(engine) as session:
        session.add_all(
            [
                AIAsset(type="dataset"),
                AIAsset(type="publication"),
                Dataset(
                    identifier="1",
                    name="Parent",
                    platform="example",
                    platform_identifier="1",
                    description="description text",
                    same_as="",
                ),
                Publication(
                    identifier="2",
                    title="A publication",
                    platform="example",
                    platform_identifier="1",
                ),
            ]
        )
        session.commit()

    body = {
        "platform": "example",
        "platform_identifier": "2",
        "description": "A description.",
        "name": "Example Dataset",
        "same_as": "https://www.example.com/dataset/example",
        "citations": [2],
        "contact": "John Doe",
        "creator": "John Doe",
        "publisher": "John Doe",
        "date_modified": "2023-01-01T15:15:00.000Z",
        "date_published": "2022-01-01T15:15:00.000Z",
        "funder": "John Doe",
        "is_accessible_for_free": True,
        "issn": "12345679",
        "size": 100,
        "spatial_coverage": "New York",
        "temporal_coverage_from": "2020-01-01T00:00:00.000Z",
        "temporal_coverage_to": "2021-01-01T00:00:00.000Z",
        "version": "1.1.0",
        "alternate_names": ["alias 1", "alias 2"],
        "distributions": [
            {
                "content_url": "https://www.example.com/dataset/file.csv",
                "content_size_kb": 10000,
                "description": "Description of this file.",
                "encoding_format": "text/csv",
                "name": "Name of this file.",
                "checksum": [{"value": "123456789abcdefg123456789abcdefg", "algorithm": "md5"}],
            }
        ],
        "is_part": [1],
        "has_parts": [],
        "license": "https://creativecommons.org/share-your-work/public-domain/cc0/",
        "keywords": ["keyword1", "keyword2"],
        "measured_values": [
            {"variable": "molecule concentration", "technique": "mass spectrometry"}
        ],
    }
    response = client.post("/datasets/v0", json=body, headers={"Authorization": "Fake token"})
    assert response.status_code == 200

    response = client.get("/datasets/v0/3")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["identifier"] == 3
    assert response_json["name"] == "Example Dataset"
    assert response_json["description"] == "A description."
    assert len(response_json["distributions"]) == 1
    assert response_json["distributions"][0]["name"] == "Name of this file."
    assert "identifier" not in response_json["distributions"][0]

    assert set(response_json["alternate_names"]) == {"alias 1", "alias 2"}
    assert response_json["citations"] == [2]
    assert len(response_json["distributions"][0]["checksum"]) == 1
    assert response_json["distributions"][0]["checksum"][0]["algorithm"] == "md5"
    assert (
        response_json["distributions"][0]["checksum"][0]["value"]
        == "123456789abcdefg123456789abcdefg"
    )
    assert "identifier" not in response_json["distributions"][0]["checksum"][0]
    assert set(response_json["is_part"]) == {1}
    assert (
        response_json["license"] == "https://creativecommons.org/share-your-work/public-domain/cc0/"
    )
    assert set(response_json["keywords"]) == {"keyword1", "keyword2"}
    assert len(response_json["measured_values"]) == 1
    assert "identifier" not in response_json["measured_values"][0]
    assert response_json["measured_values"][0]["variable"] == "molecule concentration"
    assert response_json["measured_values"][0]["technique"] == "mass spectrometry"
