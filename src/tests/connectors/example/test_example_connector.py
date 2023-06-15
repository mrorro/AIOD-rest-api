import pytest

import connectors


@pytest.mark.parametrize(
    "datatype",
    [
        "publications",
        "news",
        "events",
        "case_studies",
        "presentations",
        "projects",
        "educational_resources",
        "organisations",
    ],
)
def test_fetch_all_happy_path(datatype: str):
    connector = connectors.example_connectors[datatype]
    resources = list(connector.fetch_all(limit=None))
    assert len(resources) >= 1
    resource = resources[0]
    if hasattr(resource, "keywords"):  # otherwise, only tested that connector can run
        assert set(resource.keywords) == {"keyword1", "keyword2"}
