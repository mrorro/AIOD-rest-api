import copy
import json

import responses
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import  PublicationDescription
from tests.testutils.paths import path_test_resources

#Testing imports
import pytest

ZENODO_URL = "https://zenodo.org/api/"


def test_happy_path(client: TestClient, engine: Engine):

    publication_description = PublicationDescription(
        doi="10.5281/zenodo.7712947", node="zenodo", node_specific_identifier="7712947"
    )
    with Session(engine) as session:
        # Populate database.
        # Deepcopy necessary because SqlAlchemy changes the instance so that accessing the
        # node_specific_identifier is not possible anymore
        session.add(copy.deepcopy(publication_description))
        session.commit()
    
    with responses.RequestsMock() as mocked_requests:
        _mock_normal_responses(mocked_requests, publication_description)
        response = client.get("/nodes/zenodo/publications/7712947")

    assert response.status_code == 200
    response_json = response.json()
    
    with open(path_test_resources() / "connectors" / "zenodo" / "data_1.json", "r") as f:
        expected_info = json.load(f)
    
    assert response_json["doi"] == expected_info["doi"]
    assert response_json["title"] == expected_info["metadata"]["title"]
    



def test_publication_not_found_in_local_db(client: TestClient, engine: Engine):

    publication_description = PublicationDescription(
        doi="10.5281/zenodo.7712947", node="zenodo", node_specific_identifier="7712947"
    )
    with Session(engine) as session:
        # Populate database.
        # Deepcopy necessary because SqlAlchemy changes the instance so that accessing the
        # node_specific_identifier is not possible anymore
        session.add(copy.deepcopy(publication_description))
        session.commit()

    response = client.get("/nodes/zenodo/publications/2")  # Note that only dataset 1 exists
    assert response.status_code == 404
    assert response.json()["detail"] == "Publication '2' of 'zenodo' not found in the database."



def _mock_normal_responses(
    mocked_requests: responses.RequestsMock, publication_description: PublicationDescription
):
    """
    Mocking requests to the OpenML dependency, so that we test only our own services
    """
    with open(path_test_resources() / "connectors" / "zenodo" / "data_1.json", "r") as f:
        data_response = json.load(f)

    mocked_requests.add(
        responses.GET,
        f"{ZENODO_URL}records/{publication_description.node_specific_identifier}",
        json=data_response,
        status=200,
    )

