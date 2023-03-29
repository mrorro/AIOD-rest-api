from typing import Iterator

from connectors import ResourceConnector
from node_names import NodeName
from schemas import AIoDPublication


class ExamplePublicationConnector(ResourceConnector[AIoDPublication]):
    @property
    def node_name(self) -> NodeName:
        return NodeName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[AIoDPublication]:
        yield from [
            AIoDPublication(
                title="AMLB: an AutoML Benchmark",
                url="https://arxiv.org/abs/2207.12560",
                doi="1",
                node="example",
                node_specific_identifier="1",
            ),
            AIoDPublication(
                title="Searching for exotic particles in high-energy physics with deep learning",
                doi="2",
                node="example",
                node_specific_identifier="2",
            ),
        ][:limit]

    def fetch(self, node_specific_identifier: str) -> AIoDPublication:
        return AIoDPublication(
            doi="10.5281/zenodo.7712947",
            title="International Journal of Current Science Research and Review",
        )
