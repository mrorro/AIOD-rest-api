import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from connectors.abstract.dataset_connector import DatasetConnector
from schemas import AIoDDataset


class ExampleDatasetConnector(DatasetConnector):
    def fetch(self, node_specific_identifier: str) -> AIoDDataset:
        (dataset,) = [
            d
            for d in self.fetch_all(None)
            if d.node_specific_identifier == node_specific_identifier
        ]
        return dataset

    def fetch_all(self, limit: int | None = None) -> typing.Iterator[AIoDDataset]:
        yield from [
            AIoDDataset(
                name="Higgs",
                node="openml",
                description="Higgs dataset",
                same_as="non-existing-url/1",
                node_specific_identifier="42769",
            ),
            AIoDDataset(
                name="porto-seguro",
                node="openml",
                description="Porto seguro dataset",
                same_as="non-existing-url/2",
                node_specific_identifier="42742",
            ),
            AIoDDataset(
                name="rotten_tomatoes config:default split:train",
                node="huggingface",
                description="Rotten Tomatoes dataset train",
                same_as="non-existing-url/3",
                node_specific_identifier="rotten_tomatoes|default|train",
            ),
            AIoDDataset(
                name="rotten_tomatoes config:default split:validation",
                node="huggingface",
                description="Rotten Tomatoes dataset validation",
                same_as="non-existing-url/4",
                node_specific_identifier="rotten_tomatoes|default|validation",
            ),
            AIoDDataset(
                name="rotten_tomatoes config:default split:test",
                node="huggingface",
                description="Rotten Tomatoes dataset test",
                same_as="non-existing-url/5",
                node_specific_identifier="rotten_tomatoes|default|test",
            ),
        ][:limit]
