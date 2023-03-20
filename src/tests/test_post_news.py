import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.models import DatasetDescription


def test_happy_path(client: TestClient, engine: Engine):
    pass

def test_unicode(client: TestClient, engine: Engine, name):
    pass

def test_duplicated_news(client: TestClient, engine: Engine):
    pass


def test_missing_value(client: TestClient, engine: Engine, field: str):
   pass


def test_null_value(client: TestClient, engine: Engine, field: str):
    pass
