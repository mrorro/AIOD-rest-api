from typing import Iterator

from connectors.abstract.publication_connector import PublicationConnector
from database.model.publication import OrmPublication
from schemas import AIoDPublication


class ExamplePublicationConnector(PublicationConnector):
    def fetch_all(self, limit: int | None) -> Iterator[OrmPublication]:
        yield from [
            OrmPublication(
                title="AMLB: an AutoML Benchmark",
                url="https://arxiv.org/abs/2207.12560",
                doi="1",
                node="example",
                node_specific_identifier="1",
            ),
            OrmPublication(
                title="Searching for exotic particles in high-energy physics with deep learning",
                doi="2",
                node="example",
                node_specific_identifier="2",
            ),
        ][:limit]

    def fetch(self, publication: OrmPublication) -> AIoDPublication:
        return AIoDPublication(
            doi="10.5281/zenodo.7712947",
            title="International Journal of Current Science Research and Review",
        )
