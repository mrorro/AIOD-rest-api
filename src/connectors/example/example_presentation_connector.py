from datetime import datetime
from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.presentation.presentation import Presentation
from platform_names import PlatformName


class ExamplePresentationConnector(ResourceConnector[Presentation]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[Presentation]:
        json_data = loadJsonData("presentations.json")

        publications = [
            Presentation(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                name=item["name"],
                description=item["description"],
                url=item["url"],
                date_published=datetime.fromisoformat(item["datePublished"]),
                publisher=item["publisher"],
                author=item["author"],
                image=item["image"],
                is_accessible_for_free=item["is_accessible_for_free"],
            )
            for item in json_data
        ][:limit]

        yield from publications

    def fetch(self, platform_identifier: str) -> Presentation:
        (publication,) = [
            p for p in self.fetch_all(None) if p.resource.platform_identifier == platform_identifier
        ]
        return publication
