from datetime import datetime
from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.case_study.case_study import CaseStudy
from platform_names import PlatformName


class ExampleCaseStudyConnector(ResourceConnector[CaseStudy]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[CaseStudy]:
        json_data = loadJsonData("case_study.json")
        events = [
            CaseStudy(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                description=item["description"],
                name=item["name"],
                creator=item["creator"],
                publisher=item["publisher"],
                date_modified=datetime.fromisoformat(item["date_modified"]),
                date_published=datetime.fromisoformat(item["date_published"]),
                same_as=item["same_as"],
                url=item["url"],
                is_accessible_for_free=item["is_accessible_for_free"],
                alternate_names=[],
                keywords=[],
                business_categories=[],
                technical_categories=[],
            )
            for item in json_data
        ][:limit]

        yield from events

    def fetch(self, platform_identifier: str) -> CaseStudy:
        (publication,) = [
            c for c in self.fetch_all(None) if c.resource.platform_identifier == platform_identifier
        ]
        return publication
