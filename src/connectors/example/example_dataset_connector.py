import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from connectors import ResourceConnector
from connectors.resource_with_relations import ResourceWithRelations
from database.model.dataset.dataset import Dataset
from database.model.publication.publication import Publication
from database.model.resource import resource_create
from platform_names import PlatformName


class ExampleDatasetConnector(ResourceConnector[Dataset]):
    @property
    def resource_class(self) -> type[Dataset]:
        return Dataset

    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(
        self, limit: int | None = None
    ) -> typing.Iterator[ResourceWithRelations[Dataset]]:
        pydantic_class = resource_create(Dataset)
        pydantic_class_publication = resource_create(Publication)
        yield from [
            ResourceWithRelations[Dataset](
                resource=pydantic_class(
                    name="Higgs",
                    platform="openml",
                    description="Higgs dataset",
                    same_as="non-existing-url/1",
                    platform_identifier="42769",
                    alternate_names=[],
                    citations=[],
                    distributions=[],
                    is_part=[],
                    has_parts=[],
                    keywords=["keyword1", "keyword2"],
                    measured_values=[],
                ),
                related_resources={
                    "citations": [
                        pydantic_class_publication(
                            title=(
                                "Searching for exotic particles in high-energy physics with deep "
                                "learning"
                            ),
                            doi="2",
                            platform="example",
                            platform_identifier="2",
                            datasets=[],
                        )
                    ]
                },
            ),
            ResourceWithRelations[Dataset](
                resource=pydantic_class(
                    name="porto-seguro",
                    platform="openml",
                    description="Porto seguro dataset",
                    same_as="non-existing-url/2",
                    platform_identifier="42742",
                    alternate_names=[],
                    citations=[],
                    distributions=[],
                    is_part=[],
                    has_parts=[],
                    keywords=[],
                    measured_values=[],
                )
            ),
        ][:limit]
