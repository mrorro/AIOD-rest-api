from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.publication.publication import Publication
from platform_names import PlatformName


class ExamplePublicationConnector(ResourceConnector[Publication]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[Publication]:
        json_data = loadJsonData("publications.json")

        publications = [
            Publication(
                title=item["title"],
                url=item["url"],
                doi=item["doi"],
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
            )
            for item in json_data
        ][:limit]

        yield from publications

    def fetch(self, platform_identifier: str) -> Publication:
        (publication,) = [
            p for p in self.fetch_all(None) if p.resource.platform_identifier == platform_identifier
        ]
        return publication
