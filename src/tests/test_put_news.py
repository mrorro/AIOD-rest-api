import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import DatasetDescription


def test_happy_path(
    client: TestClient,
    engine: Engine,
    identifier: int
):
    pass

def test_non_existent(client: TestClient, engine: Engine):
    pass


def test_partial_update(client: TestClient, engine: Engine):
    pass

def test_too_long_name(client: TestClient, engine: Engine):
    pass


def _setup(engine):
    pass