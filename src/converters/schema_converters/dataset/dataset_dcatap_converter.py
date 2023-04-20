import re
from typing import Type

from converters.schema.dcat import (
    DcatApWrapper,
    DcatAPDataset,
    VCardIndividual,
    DcatAPIdentifier,
    DcatAPDistribution,
    SpdxChecksum,
    DcatLocation,
    DcatAPObject,
)
from converters.schema_converters.schema_converter import SchemaConverter
from schemas import AIoDDataset


class DatasetConverterDcatAP(SchemaConverter[AIoDDataset, DcatApWrapper]):
    """
    Convert an AIoD Dataset into a dcat-ap json-ld representation.
    """

    @property
    def schema_documentation(self) -> str:
        return (
            "The DCAT Application Profile for data portals in Europe (DCAT-AP) is a specification "
            "based on W3C's Data Catalogue vocabulary (DCAT) for describing public sector datasets "
            "in Europe. Its basic use case is to enable a cross-data portal search for datasets "
            "and make public sector data better searchable across borders and sectors. This can "
            "be achieved by the exchange of descriptions of data sets among data portals."
        )

    @property
    def to_class(self) -> Type[DcatApWrapper]:
        return DcatApWrapper

    def convert(self, aiod: AIoDDataset) -> DcatApWrapper:
        dataset = DcatAPDataset(
            id_="dataset_" + aiod.name,
            description=aiod.description,
            title=aiod.name,
            keyword=list(aiod.keywords),
            theme=[measured_value.variable for measured_value in aiod.measured_values],
            release_date=aiod.date_published,
            update_date=aiod.date_modified,
            version=aiod.version,
        )
        graph: list[DcatAPObject] = [dataset]
        if aiod.contact is not None and len(aiod.contact) > 0:
            contact = VCardIndividual(
                id_=_replace_special_chars("individual_{}".format(aiod.contact)), fn=aiod.contact
            )
            graph.append(contact)
            dataset.contact_point = [DcatAPIdentifier(id_=contact.id_)]
        if aiod.creator is not None and len(aiod.creator) > 0:
            creator = VCardIndividual(
                id_=_replace_special_chars("individual_{}".format(aiod.creator)), fn=aiod.creator
            )
            if creator.id_ not in {obj.id_ for obj in graph}:
                graph.append(creator)
            dataset.creator = [DcatAPIdentifier(id_=creator.id_)]
        if aiod.publisher is not None and len(aiod.publisher) > 0:
            publisher = VCardIndividual(
                id_=_replace_special_chars("individual_{}".format(aiod.publisher)),
                fn=aiod.publisher,
            )
            if publisher.id_ not in {obj.id_ for obj in graph}:
                graph.append(publisher)
            dataset.contact_point = [DcatAPIdentifier(id_=publisher.id_)]
        if aiod.spatial_coverage is not None:
            location = DcatLocation(id_=aiod.spatial_coverage, geometry=aiod.spatial_coverage)
            dataset.spatial_coverage = [DcatAPIdentifier(id_=location.id_)]
            graph.append(location)

        for aiod_distribution in aiod.distributions:
            checksum: SpdxChecksum | None = None
            if len(aiod_distribution.checksum) > 0:
                aiod_checksum = aiod_distribution.checksum[0]
                checksum = SpdxChecksum(
                    id_=aiod_checksum.value,
                    algorithm=aiod_checksum.algorithm,
                    checksumValue=aiod_checksum.value,
                )
                graph.append(checksum)
            distribution = DcatAPDistribution(
                id_=aiod_distribution.content_url,
                title=aiod_distribution.name,
                access_url=aiod_distribution.content_url,
                checksum=DcatAPIdentifier(id_=checksum.id_) if checksum is not None else None,
                download_url=aiod_distribution.content_url,
                description=aiod_distribution.description,
                media_type=aiod_distribution.encoding_format,
            )
            dataset.distribution.append(DcatAPIdentifier(id_=aiod_distribution.content_url))
            graph.append(distribution)
        return DcatApWrapper(graph_=graph)


def _replace_special_chars(name: str) -> str:
    """Replace special characters with underscores.

    Args:
        name: a name of a json-ld object.

    Returns:
        a sanitized version of the name
    """
    return re.sub("[^A-Za-z0-9]", "_", name)
