import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from connectors import ResourceConnector
from connectors.resource_with_relations import ResourceWithRelations
from node_names import NodeName
from schemas import AIoDDataset, AIoDPublication


class ExampleDatasetConnector(ResourceConnector[AIoDDataset]):
    @property
    def node_name(self) -> NodeName:
        return NodeName.example

    def fetch(self, node_specific_identifier: str) -> ResourceWithRelations:
        (dataset,) = [
            d
            for d in self.fetch_all(None)
            if d.resource.node_specific_identifier == node_specific_identifier
        ]
        return dataset

    def fetch_all(
        self, limit: int | None = None
    ) -> typing.Iterator[ResourceWithRelations[AIoDDataset]]:
        yield from [
            ResourceWithRelations[AIoDDataset](
                resource=AIoDDataset(
                    name="Higgs",
                    node="openml",
                    description="Higgs dataset",
                    same_as="non-existing-url/1",
                    node_specific_identifier="42769",
                    citations=[1],
                ),
                related_resources=[
                    AIoDPublication(
                        id=1,
                        title="Searching for exotic particles in high-energy physics with deep "
                        "learning",
                        doi="2",
                        node="example",
                        node_specific_identifier="2",
                    )
                ],
            ),
            ResourceWithRelations[AIoDDataset](
                resource=AIoDDataset(
                    name="porto-seguro",
                    node="openml",
                    description="Porto seguro dataset",
                    same_as="non-existing-url/2",
                    node_specific_identifier="42742",
                )
            ),
        ][:limit]
