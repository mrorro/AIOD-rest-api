import abc
from typing import Iterator

from connectors.node_names import NodeName
from database.models import PublicationDescription
from schemas import Publication


class PublicationConnector(abc.ABC):
    """For every node that offers publications, this PublicationConnector should be implemented."""

    @property
    def node_name(self) -> NodeName:
        """The node of this connector"""
        return NodeName.from_class(self.__class__)

    @abc.abstractmethod
    def fetch_all(self, limit: int | None) -> Iterator[PublicationDescription]:
        """Retrieve all publications"""
        pass

    @abc.abstractmethod
    def fetch(self, publication: PublicationDescription) -> Publication:
        """Retrieve extra metadata for this dataset"""
        pass
