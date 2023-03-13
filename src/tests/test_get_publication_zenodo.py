import copy
import json

import responses
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import  Publication
from tests.testutils.paths import path_test_resources

#Testing imports
import pytest

ZENODO_URL = "https://zenodo.org/api/"


def test_happy_path(client: TestClient, engine: Engine):

    response = client.get("/nodes/zenodo/publications/1")
    assert response.status_code == 200

