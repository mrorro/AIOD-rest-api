from typing import Iterator

from connectors.abstract.publication_connector import PublicationConnector
from database.model.publication import OrmPublication


class ExamplePublicationConnector(PublicationConnector):
    def fetch_all(self, limit: int | None) -> Iterator[OrmPublication]:
        yield from [
            OrmPublication(
                title="AMLB: an AutoML Benchmark", url="https://arxiv.org/abs/2207.12560"
            ),
            OrmPublication(
                title="Searching for exotic particles in high-energy physics with deep learning",
                url="https://www.nature.com/articles/ncomms5308",
            ),
        ][:limit]
