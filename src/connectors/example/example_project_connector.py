from datetime import datetime
from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.project.project import Project
from platform_names import PlatformName


class ExampleProjectConnector(ResourceConnector[Project]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[Project]:
        json_data = loadJsonData("projects.json")

        projects = [
            Project(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                name=item["name"],
                doi=item["doi"],
                start_date=datetime.fromisoformat(item["start_date"]),
                end_date=datetime.fromisoformat(item["end_date"]),
                founded_under=item["founded_under"],
                total_cost_euro=item["total_cost_euro"],
                eu_contribution_euro=item["eu_contribution_euro"],
                coordinated_by=item["coordinated_by"],
                project_description_title=item["project_description_title"],
                project_description_text=item["project_description_text"],
                programmes_url=item["programmes_url"],
                topic_url=item["topic_url"],
                call_for_proposal=item["call_for_proposal"],
                founding_scheme=item["founding_scheme"],
                image=item["image"],
                url=item["url"],
                keywords=[],
            )
            for item in json_data
        ][:limit]

        yield from projects

    def fetch(self, platform_identifier: str) -> Project:
        (publication,) = [
            p for p in self.fetch_all(None) if p.resource.platform_identifier == platform_identifier
        ]
        return publication
