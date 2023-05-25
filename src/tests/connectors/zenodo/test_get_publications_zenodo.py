from datetime import datetime
import responses
import connectors
from connectors.zenodo.zenodo_dataset_connector import ZenodoDatasetConnector
from platform_names import PlatformName
from tests.testutils.paths import path_test_resources


def read_file(path):
    with open(path, "r") as file:
        content = file.read()
    return content


def test_fetch_all_happy_path():
    connector =  connectors.dataset_connectors[PlatformName.zenodo]
    with responses.RequestsMock() as mocked_requests:
        mock_zenodo_responses(mocked_requests)
        datasets = list(connector.fetch_all())
    assert len(datasets) == 1
    dataset = datasets[0]
    assert dataset.name == "THE FIELD'S MALL MASS SHOOTING: EMERGENCY MEDICAL SERVICES RESPONSE"
    assert dataset.date_published == datetime(2023, 5, 6)



def mock_zenodo_responses(mocked_requests: responses.RequestsMock):
        mocked_requests.add(
        responses.GET,
        "/zenodo",
        json="{}",
        status=200,
    )