from datetime import datetime
from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.event.event import Event
from platform_names import PlatformName


class ExampleEventConnector(ResourceConnector[Event]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[Event]:
        json_data = loadJsonData("events.json")
        events = [
            Event(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                name=item["name"],
                description=item["description"],
                registration_url=item["registration_url"],
                location=item["location"],
                start_date=datetime.fromisoformat(item["start_date"]),
                end_date=datetime.fromisoformat(item["end_date"]),
                duration=item["duration"],
                status=item["status"],
                attendance_mode=item["attendance_mode"],
                type=item["type"],
                # TODO when filling sub and super events got:
                # AttributeError: 'int' object has no attribute '_sa_instance_state'
                # This is due to int is not type Event
                sub_events=[],
                super_events=[],
                # TODO Error if this fields are duplicated
                research_areas=[],
                application_areas=[],
                relevant_resources=[],
                used_resources=[],
            )
            for item in json_data
        ][:limit]

        yield from events

    def fetch(self, platform_identifier: str) -> Event:
        (publication,) = [
            e for e in self.fetch_all(None) if e.resource.platform_identifier == platform_identifier
        ]
        return publication
