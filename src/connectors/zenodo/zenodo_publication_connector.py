import datetime
from typing import Iterator
from sickle import Sickle
import xmltodict
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

    def _get_record_dictionary(self,record):
        xml_string = record.raw
        xml_dict = xmltodict.parse(xml_string)
        return xml_dict["record"]["metadata"]['oai_datacite']['payload']['resource']

    def _dataset_from_record(self,record):
        print("Dataset")


    def _software_from_record(self,record):
        print("Software")

    def _journal_article_from_record(self,record):
        print("JournalArticle")


    def _process_records_from_datetime(self,sk:Sickle,dt:datetime.datetime):
        records = sk.ListRecords(**{
            'metadataPrefix': 'oai_datacite',
            'from': dt.isoformat() ,
        })
        for record in records:   
            record_dict= self.get_record_dictionary(record)

            if(dict["resourceType"]["@resourceTypeGeneral"]=="Dataset"):
                self._dataset_from_record(record)
            elif(dict['resourceType']["@resourceTypeGeneral"]=="Software"):
                self._software_from_record(record)
            elif(dict['resourceType']["@resourceTypeGeneral"]=="JournalArticle"):
                self._journal_article_from_record(record)
        
        
    def fetch_all(self, limit: int | None = None) -> Iterator[AIoDPublication]:
        sickle = Sickle('https://zenodo.org/oai2d')
        date = datetime.datetime(2023, 5, 23, 12, 0, 0)
        self._process_records_from_datetime(sickle,date)

