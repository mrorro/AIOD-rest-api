from typing import Iterator

from connectors import ResourceConnector
from database.model.publication.publication import Publication
from platform_names import PlatformName


class ExamplePublicationConnector(ResourceConnector[Publication]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[Publication]:
        yield from [
            Publication(
                title="AMLB: an AutoML Benchmark",
                url="https://arxiv.org/abs/2207.12560",
                doi="1",
                platform="example",
                platform_identifier="1",
            ),
            Publication(
                title="Searching for exotic particles in high-energy physics with deep learning",
                doi="2",
                platform="example",
                platform_identifier="2",
            ),
        ][:limit]

    def fetch(self, platform_identifier: str) -> Publication:
        return Publication(
            doi="10.5281/zenodo.7712947",
            title="International Journal of Current Science Research and Review",
        )
