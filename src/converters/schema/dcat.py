"""
Based on DCAT Application Profile for data portals in Europe Version 2.1.1

The DCAT Application Profile for data portals in Europe (DCAT-AP) is a specification based on W3C's
Data Catalogue vocabulary (DCAT) for describing public sector datasets in Europe. Its basic use
case is to enable a cross-data portal search for datasets and make public sector data better
searchable across borders and sectors. This can be achieved by the exchange of descriptions of data
sets among data portals
"""
import datetime
from abc import ABC
from typing import Union

from pydantic import BaseModel, Field, Extra


class DcatAPContext(BaseModel):
    dcat: str = Field(default="http://www.w3.org/ns/dcat", const=True)
    dct: str = Field(default="http://purl.org/dc/terms/", const=True)
    vcard: str = Field(default="https://www.w3.org/2006/vcard/ns#", const=True)


class DcatAPObject(BaseModel, ABC):
    """Base class for all DCAT-AP objects"""

    id_: str = Field(alias="@id")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True


class VCardIndividual(DcatAPObject):
    type_: str = Field(default="vcard:Individual", alias="@type", const=True)
    fn: str = Field(
        alias="vcard:fn", description="The formatted text corresponding to the name of the object"
    )


class VCardOrganisation(DcatAPObject):
    type_: str = Field(default="vcard:Organisation", alias="@type", const=True)
    fn: str = Field(
        alias="vcard:fn", description="The formatted text corresponding to the name of the object"
    )


class DcatLocation(DcatAPObject):
    type_: str = Field(default="dct:Location", alias="@type", const=True)
    bounding_box: str = Field(alias="dcat:bbox", default=None)
    centroid: str = Field(alias="dcat:centroid", default=None)
    geometry: str = Field(alias="dcat:geometry", default=None)


class SpdxChecksum(DcatAPObject):
    type_: str = Field(default="spdx:Checksum", alias="@type", const=True)
    algorithm: str = Field()
    checksumValue: str = Field()


class DcatAPIdentifier(DcatAPObject):
    """Identifying another DcatAPObject. Contains only an id."""


class DcatAPDistribution(DcatAPObject):
    type_: str = Field(default="dcat:Distribution", alias="@type", const=True)
    access_url: str = Field(alias="dcat:accessURL", default=None)
    byte_size: int | None = Field(alias="dcat:byteSize", default=None)
    checksum: DcatAPIdentifier | None = Field(alias="spdx:checksum", default=None)
    description: str | None = Field(alias="dct:description", default=None)
    download_url: str | None = Field(alias="dcat:downloadURL", default=None)
    media_type: str | None = Field(alias="dcat:mediaType", default=None)
    title: str | None = Field(alias="dct:title", default=None)


class DcatAPDataset(DcatAPObject):
    type_: str = Field(default="dcat:Dataset", alias="@type", const=True)
    description: str = Field(
        alias="dct:description",
        description="This property contains a free-text account of the Dataset",
    )
    title: str = Field(
        alias="dct:title",
        description="This property contains a name given to the Dataset",
    )
    contact_point: list[DcatAPIdentifier] = Field(
        alias="dcat:contactPoint",
        description="This property contains contact information that can be used for sending "
        "comments about the Dataset.",
        default_factory=list,
    )
    distribution: list[DcatAPIdentifier] = Field(
        alias="dcat:distribution",
        description="This property links the Dataset to an available Distribution.",
        default_factory=list,
    )
    keyword: list[str] = Field(
        alias="dcat:keyword",
        description="This property contains a keyword or tag describing the Dataset",
        default_factory=list,
    )
    publisher: DcatAPIdentifier | None = Field(
        alias="dct:publisher",
        description="This property refers to an entity (organisation) responsible for making the "
        "Dataset available.",
    )
    spatial_coverage: list[DcatAPIdentifier] = Field(
        alias="dct:spatial",
        description="This property refers to a "
        "geographic region that is covered "
        "by the Dataset.",
        default_factory=list,
    )
    theme: list[str] = Field(
        alias="dcat:theme",
        description="This property refers to a category of the Dataset. A Dataset may be "
        "associated with multiple themes.",
        default_factory=list,
    )

    creator: list[DcatAPIdentifier] = Field(alias="dcat:creator", default_factory=list)
    documentation: list[DcatAPIdentifier] = Field(alias="foaf:page", default_factory=list)
    release_date: datetime.datetime | datetime.date | None = Field(alias="dct:issued")
    update_date: datetime.datetime | datetime.date | None = Field(alias="dct:modified")
    version: str | None = Field(alias="owl:versionInfo")


class DcatApWrapper(BaseModel):
    """The resulting class, containing a dataset and related entities in the graph"""

    context_: DcatAPContext = Field(default=DcatAPContext(), alias="@context", const=True)
    # instead of list[DcatAPObject], a union with all the possible values is necessary. See
    # https://stackoverflow.com/questions/58301364/pydantic-and-subclasses-of-abstract-class
    graph_: list[
        Union[
            DcatAPDataset,
            DcatAPDistribution,
            DcatLocation,
            SpdxChecksum,
            VCardOrganisation,
            VCardIndividual,
        ]
    ] = Field(alias="@graph")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True
