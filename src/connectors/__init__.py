import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import platform_names  # noqa:F401
import schemas  # noqa:F401
from .abstract.resource_connector import ResourceConnector  # noqa:F401
from .example.example_dataset_connector import ExampleDatasetConnector
from .example.example_publication_connector import ExamplePublicationConnector
from .huggingface.huggingface_dataset_connector import HuggingFaceDatasetConnector
from .openml.openml_dataset_connector import OpenMlDatasetConnector
from .zenodo.zenodo_connector import ZenodoConnector

dataset_connectors = {
    c.platform_name: c
    for c in (ExampleDatasetConnector(), OpenMlDatasetConnector(), HuggingFaceDatasetConnector())
}  # type: typing.Dict[platform_names.PlatformName, ResourceConnector[schemas.AIoDDataset]]

publication_connectors = {
    p.platform_name: p for p in (ExamplePublicationConnector(), ZenodoConnector())
}  # type: typing.Dict[platform_names.PlatformName, ResourceConnector[schemas.AIoDPublication]]
