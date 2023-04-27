"""
Fixtures that provide default instances for AIoD and ORM classes.

This way you have easy access to, for instance, an AIoDDataset filled with default values.
"""


import datetime

import pytest

from database.model.case_study import OrmCaseStudy
from database.model.dataset import OrmDataset, OrmDataDownload
from database.model.presentation import OrmPresentation
from database.model.publication import OrmPublication

from schemas import (
    AIoDCaseStudy,
    AIoDDataset,
    AIoDDistribution,
    AIoDMeasurementValue,
    AIoDChecksum,
    AIoDPresentation,
)


@pytest.fixture(scope="session")
def aiod_case_study() -> AIoDCaseStudy:
    return AIoDCaseStudy(
        identifier=7,
        description="description",
        name="name1",
        platform="platform",
        platform_identifier="1",
        same_as="same_as",
        creator="creator",
        date_modified=datetime.date(2002, 1, 1),
        date_published=datetime.datetime(2001, 1, 1, 8),
        is_accessible_for_free=True,
        alternate_names=["alternative_1", "alternative_2"],
        business_categories=["business-cat1", "business-cat2"],
        keywords=["a", "b", "c"],
        technical_categories=["technical-cat1", "technical-cat2"],
    )


@pytest.fixture(scope="session")
def orm_case_study() -> OrmCaseStudy:
    return OrmCaseStudy(
        description="description",
        name="name2",
        platform="example",
        platform_identifier="1",
        same_as="same_as",
        creator="creator",
        date_modified=datetime.datetime(2002, 1, 1),
        date_published=datetime.datetime(2001, 1, 1),
        is_accessible_for_free=True,
        alternate_names=[],
        business_categories=[],
        keywords=[],
        technical_categories=[],
    )


@pytest.fixture(scope="session")
def aiod_dataset() -> AIoDDataset:
    return AIoDDataset(
        identifier=7,
        description="description",
        name="name1",
        platform="platform",
        platformIdentifier="1",
        sameAs="sameAs",
        contact="contact",
        creator="creator",
        dateModified=datetime.date(2002, 1, 1),
        datePublished=datetime.datetime(2001, 1, 1, 8),
        funder="funder",
        isAccessibleForFree=True,
        issn="12345678",
        size=100,
        spatialCoverage="spatial_coverage",
        temporalCoverageFrom=datetime.date(2000, 1, 1),
        temporalCoverageTo=datetime.datetime(2000, 1, 2, 6),
        version="version1",
        license="license.name",
        hasParts=[],
        isPart=[],
        alternateNames=["alternative_1", "alternative_2"],
        citations=[],
        distributions=[
            AIoDDistribution(
                contentUrl="distr.content_url",
                contentSizeKb=123,
                description="distr.description",
                name="distr.name",
                encodingFormat="distr.encoding_format",
                checksum=[AIoDChecksum(algorithm="md5", value="md5hash")],
            )
        ],
        keywords=["a", "b", "c"],
        measuredValues=[AIoDMeasurementValue(variable="variable", technique="technique")],
    )


@pytest.fixture(scope="session")
def orm_dataset() -> OrmDataset:
    return OrmDataset(
        description="description",
        name="name2",
        platform="example",
        platform_identifier="1",
        same_as="sameAs",
        creator="creator",
        date_modified=datetime.datetime(2002, 1, 1),
        date_published=datetime.datetime(2001, 1, 1),
        funder="funder",
        is_accessible_for_free=True,
        issn="12345678",
        size=100,
        spatial_coverage="spatial_coverage",
        temporal_coverage_from=datetime.datetime(2000, 1, 1),
        temporal_coverage_to=datetime.datetime(2000, 1, 2),
        version="version2",
        license=None,
        has_parts=[],
        is_part=[],
        alternate_names=[],
        citations=[],
        distributions=[],
        keywords=[],
        measured_values=[],
    )


@pytest.fixture(scope="session")
def orm_data_download() -> OrmDataDownload:
    return OrmDataDownload(
        content_url="url",
        content_size_kb=128,
        description="description",
        encoding_format="text/csv",
        name="name",
    )


@pytest.fixture(scope="session")
def orm_publication() -> OrmPublication:
    return OrmPublication(
        title="Title",
        doi="12345678",
        platform="example",
        platform_identifier="2",
        datasets=[],
    )


@pytest.fixture(scope="session")
def aiod_presentation() -> AIoDPresentation:
    return AIoDPresentation(
        identifier=9,
        name="name1",
        platform="platform",
        platform_identifier="1",
        author="author1",
        datePublished=datetime.datetime(2001, 1, 1, 8),
        description="description",
        image="url_of_the_image",
        is_accessible_for_free=False,
        publisher="publisher",
        url="url_of_the_resource",
    )


@pytest.fixture(scope="session")
def orm_presentation() -> OrmPresentation:
    return OrmPresentation(
        name="name2",
        platform="platform2",
        platform_identifier="2",
        author="author2",
        datePublished=datetime.datetime(2001, 1, 1, 8),
        description="description2",
        image="url_of_the_image2",
        is_accessible_for_free=False,
        publisher="publisher2",
        url="url_of_the_resource2",
    )
