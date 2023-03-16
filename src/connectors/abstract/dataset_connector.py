import abc
from typing import Iterator

from connectors.node_names import NodeName
from database.models import OrmDataset


class DatasetConnector(abc.ABC):
    """For every node that offers datasets, this DatasetConnector should be implemented."""

    @property
    def node_name(self) -> NodeName:
        """The node of this connector"""
        return NodeName.from_class(self.__class__)

    @abc.abstractmethod
    def fetch(self, node_specific_identifier: str) -> OrmDataset:
        """Retrieve information of specific dataset"""
        pass

    @abc.abstractmethod
    def fetch_all(self, limit: int | None = None) -> Iterator[OrmDataset]:
        """Retrieve information of all datasets"""
        pass
