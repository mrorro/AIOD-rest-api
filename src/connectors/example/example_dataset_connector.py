import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from connectors import ResourceConnector
from connectors.resource_with_relations import ResourceWithRelations
from database.model.dataset.dataset import Dataset
from database.model.publication.publication import Publication
from platform_names import PlatformName


class ExampleDatasetConnector(ResourceConnector[Dataset]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch(self, platform_identifier: str) -> ResourceWithRelations:
        (dataset,) = [
            d for d in self.fetch_all(None) if d.resource.platform_identifier == platform_identifier
        ]
        return dataset

    def fetch_all(
        self, limit: int | None = None
    ) -> typing.Iterator[ResourceWithRelations[Dataset]]:
        yield from [
            ResourceWithRelations[Dataset](
                resource=Dataset(
                    name="Higgs",
                    platform="openml",
                    description="Higgs dataset",
                    same_as="non-existing-url/1",
                    platform_identifier="42769",
                ),
                related_resources={
                    "citations": [
                        Publication(
                            title=(
                                "Searching for exotic particles in high-energy physics with deep "
                                "learning"
                            ),
                            doi="2",
                            platform="example",
                            platform_identifier="2",
                        )
                    ]
                },
            ),
            ResourceWithRelations[Dataset](
                resource=Dataset(
                    name="porto-seguro",
                    platform="openml",
                    description="Porto seguro dataset",
                    same_as="non-existing-url/2",
                    platform_identifier="42742",
                )
            ),
        ][:limit]
