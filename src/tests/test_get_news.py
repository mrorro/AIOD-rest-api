from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient



def test_happy_path(client: TestClient, engine: Engine):
    pass