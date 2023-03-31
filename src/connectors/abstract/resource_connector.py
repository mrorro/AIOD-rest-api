import abc
from typing import Generic, TypeVar, Iterator

from connectors.resource_with_relations import ResourceWithRelations
from node_names import NodeName
from schemas import AIoDAIResource

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDAIResource)


class ResourceConnector(abc.ABC, Generic[AIOD_CLASS]):
    """For every node that offers this resource, this ResourceConnector should be implemented."""

    @property
    @abc.abstractmethod
    def node_name(self) -> NodeName:
        """The node of this connector"""
        pass

    @abc.abstractmethod
    def fetch(
        self, node_specific_identifier: str
    ) -> AIOD_CLASS | ResourceWithRelations[AIOD_CLASS]:
        """Retrieve information of specific resource"""
        pass

    @abc.abstractmethod
    def fetch_all(
        self, limit: int | None = None
    ) -> Iterator[AIOD_CLASS | ResourceWithRelations[AIOD_CLASS]]:
        """Retrieve information of all resources"""
        pass
