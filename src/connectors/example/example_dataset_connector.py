import typing

from connectors.abstract.dataset_connector import DatasetConnector
from database.models import DatasetDescription


class ExampleDatasetConnector(DatasetConnector):
    def fetch(self, node_specific_identifier: str) -> DatasetDescription:
        (dataset,) = [
            d
            for d in self.fetch_all(None)
            if d.node_specific_identifier == node_specific_identifier
        ]
        return dataset

    def fetch_all(self, limit: int | None = None) -> typing.Iterator[DatasetDescription]:
        yield from [
            DatasetDescription(
                name="Higgs",
                node="openml",
                description="Higgs dataset",
                same_as="non-existing-url/1",
                node_specific_identifier="42769",
            ),
            DatasetDescription(
                name="porto-seguro",
                node="openml",
                description="Porto seguro dataset",
                same_as="non-existing-url/2",
                node_specific_identifier="42742",
            ),
            DatasetDescription(
                name="rotten_tomatoes config:default split:train",
                node="huggingface",
                description="Rotten Tomatoes dataset train",
                same_as="non-existing-url/3",
                node_specific_identifier="rotten_tomatoes|default|train",
            ),
            DatasetDescription(
                name="rotten_tomatoes config:default split:validation",
                node="huggingface",
                description="Rotten Tomatoes dataset validation",
                same_as="non-existing-url/4",
                node_specific_identifier="rotten_tomatoes|default|validation",
            ),
            DatasetDescription(
                name="rotten_tomatoes config:default split:test",
                node="huggingface",
                description="Rotten Tomatoes dataset test",
                same_as="non-existing-url/5",
                node_specific_identifier="rotten_tomatoes|default|test",
            ),
        ][:limit]
