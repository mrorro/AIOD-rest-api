import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

import node_names  # noqa:F401
import schemas  # noqa:F401
from .abstract.resource_connector import ResourceConnector  # noqa:F401
from .example.example_dataset_connector import ExampleDatasetConnector
from .example.example_publication_connector import ExamplePublicationConnector
from .huggingface.huggingface_dataset_connector import HuggingFaceDatasetConnector
from .openml.openml_dataset_connector import OpenMlDatasetConnector
from .zenodo.zenodo_publication_connector import ZenodoPublicationConnector

dataset_connectors = {
    c.node_name: c
    for c in (ExampleDatasetConnector(), OpenMlDatasetConnector(), HuggingFaceDatasetConnector())
}  # type: typing.Dict[node_names.NodeName, ResourceConnector[schemas.AIoDDataset]]

publication_connectors = {
    p.node_name: p for p in (ExamplePublicationConnector(), ZenodoPublicationConnector())
}  # type: typing.Dict[node_names.NodeName, ResourceConnector[schemas.AIoDPublication]]
