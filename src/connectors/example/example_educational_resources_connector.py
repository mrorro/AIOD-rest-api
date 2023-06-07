from datetime import datetime
from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.educational_resource.educational_resource import EducationalResource
from platform_names import PlatformName


class ExampleEducationalResourceConnector(ResourceConnector[EducationalResource]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[EducationalResource]:
        json_data = loadJsonData("educational_resources.json")
        educational_resources = [
            EducationalResource(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                title=item["title"],
                date_modified=datetime.fromisoformat(item["date_modified"]),
                body=item["body"],
                website_url=item["website_url"],
                educational_level=item["educational_level"],
                educational_type=item["educational_type"],
                pace=item["pace"],
                interactivity_type=item["interactivity_type"],
                typical_age_range=item["typical_age_range"],
                accessibility_api=item["accessibility_api"],
                accessibility_control=item["accessibility_control"],
                access_mode=item["access_mode"],
                access_mode_sufficient=item["access_mode_sufficient"],
                access_restrictions=item["access_restrictions"],
                citations=item["citations"],
                version=item["version"],
                number_of_weeks=item["number_of_weeks"],
                field_prerequisites=item["field_prerequisites"],
                short_summary=item["short_summary"],
                duration_minutes_and_hours=item["duration_minutes_and_hours"],
                hours_per_week=item["hours_per_week"],
                country=item["country"],
                is_accessible_for_free=item["is_accessible_for_free"],
                credits=item["credits"],
                duration_in_years=item["duration_in_years"],
                languages=[],
                target_audience=[],
                keywords=[],
            )
            for item in json_data
        ][:limit]

        yield from educational_resources

    def fetch(self, platform_identifier: str) -> EducationalResource:
        (publication,) = [
            e for e in self.fetch_all(None) if e.resource.platform_identifier == platform_identifier
        ]
        return publication
