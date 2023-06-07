from .abstract.resource_connector import ResourceConnector  # noqa:F401
from .example.example_dataset_connector import ExampleDatasetConnector
from .example.example_publication_connector import ExamplePublicationConnector
from .huggingface.huggingface_dataset_connector import HuggingFaceDatasetConnector
from .openml.openml_dataset_connector import OpenMlDatasetConnector
from .zenodo.zenodo_dataset_connector import ZenodoDatasetConnector
from .example.example_news_connector import ExampleNewsConnector
from .example.example_event_connector import ExampleEventConnector
from .example.example_case_study_connector import ExampleCaseStudyConnector
from .example.example_presentation_connector import ExamplePresentationConnector

dataset_connectors = {
    c.platform_name: c
    for c in (
        ExampleDatasetConnector(),
        OpenMlDatasetConnector(),
        HuggingFaceDatasetConnector(),
        ZenodoDatasetConnector(),
    )
}

# publication_connectors = {p.platform_name: p for p in ([])}

example_connectors = {
    "publications": ExamplePublicationConnector(),
    "news": ExampleNewsConnector(),
    "events": ExampleEventConnector(),
    "case_study": ExampleCaseStudyConnector(),
    "presentations": ExamplePresentationConnector(),
}
