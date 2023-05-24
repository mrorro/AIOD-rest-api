from datetime import datetime
import connectors
from connectors.zenodo.zenodo_dataset_connector import ZenodoDatasetConnector
from platform_names import PlatformName
from tests.testutils.paths import path_test_resources





def read_file(path):
    with open(path, 'r') as file:
        content = file.read()
    return content


class MockRecord:
    def __init__(self, raw):
        self.raw = raw



def mock_list_records(**kwargs):
    # Aquí puedes simular los registros que deseas devolver
    # como si estuvieran siendo devueltos por Sickle
    mock_records = [
        MockRecord(read_file(path_test_resources()+"connectors/zenodo/article_example.xml")),  # Ejemplo de registro 1
        MockRecord(read_file(path_test_resources()+"connectors/zenodo/dataset_example.xml")),  # Ejemplo de registro 2
    ]
    return mock_records

def mock_sickle_ListRecords(*args, **kwargs):
    return mock_list_records(**kwargs)

def mock_sickle(**kwargs):
    class MockSickle:
        def __init__(self, *args, **kwargs):
            pass

        def ListRecords(self, *args, **kwargs):
            return mock_sickle_ListRecords(*args, **kwargs)

    return MockSickle(**kwargs)



def process_dataset_record():
    connector = connectors.dataset_connectors[PlatformName.zenodo]
    sickle = mock_sickle()
    date = datetime(2023, 5, 24, 5, 0, 0)
    datasets = connector._retrieve_dataset_from_datetime(sickle, date)
    assert len(datasets) == 1




