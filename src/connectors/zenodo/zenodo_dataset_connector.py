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
        raise Exception("Not implemented")
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
            creators_list = [item["creatorName"] for item in record["creators"]["creator"]]
            creator =  ", ".join(creators_list) #TODO change field to an array
        elif(isinstance(record["creators"]["creator"]['creatorName'],str)):
            creator = record["creators"]["creator"]['creatorName']
    
        #Get dataset title
        title=""
        if(isinstance(record["titles"]["title"],str)):
            title =record["titles"]["title"]
    
        #Get dataset description
        description =""
        if(isinstance(record["descriptions"]["description"], list)):
            for element in record["descriptions"]["description"]:
                if element.get('@descriptionType') == 'Abstract':
                    description = element.get('#text')
                    break
        elif(record["descriptions"]["description"]['@descriptionType']== 'Abstract'):
            description =record["descriptions"]["description"]['#text']
 
        #Get publication date 
        date_published = None
        date_format = "%Y-%m-%d"
        if(isinstance(record["dates"]["date"], list)):
            for element in record["dates"]["date"]:
                if element.get('@dateType') == 'Issued':
                    date_string=element['#text']
                    date_published = datetime.strptime(date_string, date_format)
                    break
        elif(record["dates"]["date"]['@dateType']== 'Issued'):
            date_string=record["dates"]["date"]['#text']
            date_published = datetime.strptime(date_string, date_format)
        
        
        #Get dataset publisher
        publisher=""
        if(isinstance(record["publisher"]),str):
            publisher= record["publisher"]

        #Get dataset keywords
        keywords=[]

        if "subjects" in record:
            print(record["subjects"]["subject"])
            if (isinstance(record["subjects"]["subject"], str)):
                keywords=[record["subjects"]["subject"]]
            elif(isinstance(record["subjects"]["subject"], list)):
                keywords = [item for item in record["subjects"]["subject"] if isinstance(item, str)]

     
        dataset= AIoDDataset(
            ame=title[:150],
            same_as="",
            creator= creator[:150],#TODO not enough characters for creator list, change to array or allow more length
            description=description[:500],
            date_published=date_published,
            publisher=publisher,
            keywords=keywords,
        ) 
        return dataset



    def _retrieve_dataset_from_datetime(self,sk:Sickle,dt:datetime.datetime):
        records = sk.ListRecords(**{
            'metadataPrefix': 'oai_datacite',
            'from': dt.isoformat() ,
        })
        list_datasets = []
        for record in records:   
            record_dict= self.get_record_dictionary(record)

            if(record_dict["resourceType"]["@resourceTypeGeneral"]=="Dataset"):
                list_datasets.append(self._dataset_from_record(record_dict))

        return list
        
    def fetch_all(self, limit: int | None = None) -> Iterator[AIoDPublication]:
        sickle = Sickle('https://zenodo.org/oai2d')
        date = datetime.datetime(2000, 5, 23, 12, 0, 0)#this should be a paramater
        return self._retrieve_dataset_from_datetime(sickle,date)

