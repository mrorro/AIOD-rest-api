import abc
from typing import Generic, TypeVar, Iterator

from connectors.resource_with_relations import ResourceWithRelations
from platform_names import PlatformName
from schemas import AIoDAIResource

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDAIResource)


class ResourceConnector(abc.ABC, Generic[AIOD_CLASS]):
    """
    For every platform that offers this resource, this ResourceConnector should be implemented.
    """

    @property
    @abc.abstractmethod
    def platform_name(self) -> PlatformName:
        """The platform of this connector"""
        pass

    @abc.abstractmethod
    def fetch(self, platform_identifier: str) -> AIOD_CLASS | ResourceWithRelations[AIOD_CLASS]:
        """Retrieve information of specific resource"""
        pass

    @abc.abstractmethod
    def fetch_all(
        self, limit: int | None = None
    ) -> Iterator[AIOD_CLASS | ResourceWithRelations[AIOD_CLASS]]:
        """Retrieve information of all resources"""
        pass
