from typing import Iterator
from fastapi import HTTPException

import requests

from connectors.abstract.publication_connector import PublicationConnector
from database.model.publication import OrmPublication
from schemas import AIoDPublication


class ZenodoPublicationConnector(PublicationConnector):
    def fetch(self, publication: OrmPublication) -> AIoDPublication:
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
        result = AIoDPublication(
            doi=publication_json["doi"],
            title=publication_json["metadata"]["title"],
            node=publication.node,
            node_specific_identifier=publication.node_specific_identifier,
        )
        return result

    def fetch_all(self, limit: int | None) -> Iterator[OrmPublication]:
        url_data = "https://zenodo.org/api/records/"
        response = requests.get(url_data, params={"type": "publication"})
        response_json = response.json()
        if not response.ok:
            msg = response_json["error"]["message"]
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error while fetching data from Zenodo: '{msg}'",
            )
        for publication_json in response_json["hits"]["hits"]:
            yield OrmPublication(
                doi=publication_json["doi"],
                title=publication_json["metadata"]["title"],
                node=self.node_name,
                node_specific_identifier=str(publication_json["id"]),
            )
