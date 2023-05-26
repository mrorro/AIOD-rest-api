import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import platform_names  # noqa:F401
from database.model.dataset import Dataset  # noqa:F401
from .abstract.resource_connector import ResourceConnector  # noqa:F401
from .example.example_dataset_connector import ExampleDatasetConnector
from .huggingface.huggingface_dataset_connector import HuggingFaceDatasetConnector
from .openml.openml_dataset_connector import OpenMlDatasetConnector

dataset_connectors = {
    c.platform_name: c
    for c in (ExampleDatasetConnector(), OpenMlDatasetConnector(), HuggingFaceDatasetConnector())
}  # type: typing.Dict[platform_names.PlatformName, ResourceConnector[Dataset]]

# publication_connectors = {
#     p.platform_name: p for p in (ExamplePublicationConnector(), ZenodoPublicationConnector())
# }  # type: typing.Dict[platform_names.PlatformName, ResourceConnector[schemas.AIoDPublication]]
