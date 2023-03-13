from typing import Iterator
from fastapi import HTTPException

import requests

from connectors.abstract.publication_connector import PublicationConnector
from database.models import PublicationDescription
from schemas import Publication


class ZenodoPublicationConnector(PublicationConnector):
    def fetch(self, publication: PublicationDescription) -> Publication:
        identifier = publication.node_specific_identifier
        url_data = f"https://zenodo.org/api/records/{identifier}"
        response = requests.get(url_data)
        if not response.ok:
            code = response.status_code
            msg = response.json()["message"]
            raise HTTPException(
                status_code=code,
                detail=f"Error while fetching data from Zenodo: '{msg}'",
            )
        publication_json = response.json()
        result = Publication(
            doi=publication_json["doi"], title=publication_json["metadata"]["title"]
        )
        return result

    def fetch_all(self, limit: int | None) -> Iterator[PublicationDescription]:
        yield from [
            PublicationDescription(
                doi="10.5281/zenodo.7712947", node="zenodo", node_specific_identifier="7712947"
            ),
            PublicationDescription(
                doi=" 10.5281/zenodo.6306305", node="zenodo", node_specific_identifier="6306305"
            ),
        ][:limit]
