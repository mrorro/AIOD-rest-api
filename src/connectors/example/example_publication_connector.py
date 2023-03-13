from typing import Iterator

from connectors.abstract.publication_connector import PublicationConnector
from database.models import PublicationDescription
from schemas import Publication


class ExamplePublicationConnector(PublicationConnector):
    def fetch_all(self, limit: int | None) -> Iterator[PublicationDescription]:
        yield from [
            
            PublicationDescription(
                doi="10.5281/zenodo.7712947",
                node="zenodo",
                node_specific_identifier="7712947"
            ),
            PublicationDescription(
                doi=" 10.5281/zenodo.6306305",
                node="zenodo",
                node_specific_identifier="6306305"
            ),
           
        ][:limit]
    def fetch(self, publication: PublicationDescription) -> Publication:
        return  Publication(
            doi="10.5281/zenodo.7712947",
            title="International Journal of Current Science Research and Review",

            
        )
