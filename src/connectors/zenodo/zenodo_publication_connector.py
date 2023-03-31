from typing import Iterator

import requests
from fastapi import HTTPException

from connectors import ResourceConnector
from platform_names import PlatformName
from schemas import AIoDPublication


class ZenodoPublicationConnector(ResourceConnector[AIoDPublication]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.zenodo

    def fetch(self, platform_identifier: str) -> AIoDPublication:
        identifier = platform_identifier
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
            platform=self.platform_name,
            platform_identifier=platform_identifier,
        )
        return result

    def fetch_all(self, limit: int | None = None) -> Iterator[AIoDPublication]:
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
            yield AIoDPublication(
                doi=publication_json["doi"],
                title=publication_json["metadata"]["title"],
                platform=self.platform_name,
                platform_identifier=str(publication_json["id"]),
            )
