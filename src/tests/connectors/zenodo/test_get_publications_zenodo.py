from datetime import datetime
from typing import cast
import connectors
from connectors.zenodo.zenodo_dataset_connector import ZenodoDatasetConnector
from platform_names import PlatformName
from tests.testutils.paths import path_test_resources


def read_file(path):
    with open(path, "r") as file:
        content = file.read()
    return content


class MockRecord:
    def __init__(self, raw):
        self.raw = raw


class MockSickle:
    def ListRecords(self, **kwargs):
        mock_records = [
            MockRecord(read_file(path_test_resources() / "connectors/zenodo/article_example.xml")),
            MockRecord(read_file(path_test_resources() / "connectors/zenodo/dataset_example.xml")),
        ]
        return mock_records


def test_process_dataset_record():
    connector = cast(ZenodoDatasetConnector, connectors.dataset_connectors[PlatformName.zenodo])
    sickle = MockSickle()
    date = datetime(2023, 5, 24, 5, 0, 0)
    datasets = list(connector._retrieve_dataset_from_datetime(sickle, date))
    assert len(datasets) == 1
    dataset = datasets[0]
    assert dataset.name == "THE FIELD'S MALL MASS SHOOTING: EMERGENCY MEDICAL SERVICES RESPONSE"
    assert dataset.date_published == datetime(2023, 5, 6)
