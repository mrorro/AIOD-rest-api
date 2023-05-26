import abc
from typing import Generic, TypeVar, Iterator

from sqlmodel import SQLModel

from connectors.resource_with_relations import ResourceWithRelations
from platform_names import PlatformName


RESOURCE = TypeVar("RESOURCE", bound=SQLModel)


class ResourceConnector(abc.ABC, Generic[RESOURCE]):
    """
    For every platform that offers this resource, this ResourceConnector should be implemented.
    """

    @property
    @abc.abstractmethod
    def platform_name(self) -> PlatformName:
        """The platform of this connector"""
        pass

    @abc.abstractmethod
    def fetch(self, platform_identifier: str) -> RESOURCE | ResourceWithRelations[RESOURCE]:
        """Retrieve information of specific resource"""
        pass

    @abc.abstractmethod
    def fetch_all(
        self, limit: int | None = None
    ) -> Iterator[RESOURCE | ResourceWithRelations[RESOURCE]]:
        """Retrieve information of all resources"""
        pass
