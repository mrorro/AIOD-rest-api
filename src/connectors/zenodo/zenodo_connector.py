import datetime
from typing import Iterator
from sickle import Sickle
import xmltodict
import requests
from fastapi import HTTPException

from connectors import ResourceConnector
from platform_names import PlatformName
from schemas import AIoDDataset, AIoDPublication


class ZenodoConnector(ResourceConnector[AIoDPublication]):
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

    def _dataset_from_record(self,record)->AIoDDataset:
        #Get creator name
        creator =""
        if(isinstance(record["creators"]["creator"], list)):
            creator = record["creators"]["creator"][0]['creatorName']
        else:
            creator = record["creators"]["creator"]['creatorName']
    
        #Get dataset title
        title =record["titles"]["title"]
    
        #Get dataset description
        description =""
        if(isinstance(record["descriptions"]["description"], list)):
            description=record["descriptions"]["description"][0]['#text']
        else:
            description =record["descriptions"]["description"]['#text']

        #Get publication date 
        date_published = None
        date_format = "%Y-%m-%d"
        if(isinstance(record["dates"]["date"], list)):
            date_string=record["dates"]["date"][0]['#text']
            date_published = datetime.strptime(date_string, date_format)
        else:
            date_string=record["dates"]["date"]['#text']
            date_published = datetime.strptime(date_string, date_format)
        
        #Get dataset publisher
        publisher= record["publisher"]

        #Get dataset keywords
        keywords=[]

        if "subjects" in record:
            if(isinstance(record["subjects"]["subject"], list)):
                keywords=record["subjects"]["subject"]
            else:
                keywords=[record["subjects"]["subject"]]
     
        dataset= AIoDDataset(
            ame=title[:150],
            same_as="",
            creator= creator,
            description=description[:500],
            date_published=date_published,
            publisher=publisher,
            keywords=keywords,
        ) 
        return dataset


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
        date = datetime.datetime(2000, 5, 23, 12, 0, 0)#this should be a paramater
        self._process_records_from_datetime(sickle,date)

