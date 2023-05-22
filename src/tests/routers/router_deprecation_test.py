import datetime
import tempfile

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from tests.testutils.test_resource import OrmTestResource, AIoDTestResource, RouterTestResource
from authentication import keycloak_openid


class DeprecatedRouter(RouterTestResource):
    """A deprecated router, just used for testing."""

    @property
    def version(self) -> int:
        return 1

    @property
    def deprecated_from(self, date=datetime.date(2022, 4, 21)) -> datetime.date | None:
        return date


@pytest.mark.parametrize(
    "verb,url",
    [
        ("get", "/test_resources/v1/"),
        ("get", "/platforms/example/test_resources/v1"),
        ("get", "/test_resources/v1/1"),
        ("get", "/platforms/example/test_resources/v1/1"),
        ("post", "/test_resources/v1/"),
        ("put", "/test_resources/v1/1"),
        ("delete", "/test_resources/v1/1"),
    ],
)
def test_deprecated_router(verb: str, url: str, mocked_previlege_token):

    keycloak_openid.decode_token = mocked_previlege_token

    temporary_file = tempfile.NamedTemporaryFile()
    engine = create_engine(f"sqlite:///{temporary_file.name}")
    OrmTestResource.metadata.create_all(engine)

    test_instance = OrmTestResource(title="A title", platform="example", platform_identifier="1")

    with Session(engine) as session:
        session.add(test_instance)
        session.commit()

    app = FastAPI()
    app.include_router(DeprecatedRouter().create(engine, ""))
    client = TestClient(app)

    kwargs = {}
    if verb in ("post", "put"):
        kwargs = {
            "json": AIoDTestResource(
                title="Another title", platform="example", platform_identifier="2"
            ).dict(),
            "headers": {"Authorization": "fake-token"},
        }
    response = getattr(client, verb)(url, **kwargs)
    assert response.status_code == 200
    assert "deprecated" in response.headers
    assert response.headers.get("deprecated") == "Thu, 21 Apr 2022 00:00:00 GMT"
