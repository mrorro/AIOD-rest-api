from sqlalchemy import Table, Column, ForeignKey

from database.model.base import Base


dataset_alternateName_relationship = Table(
    "dataset_alternateName",
    Base.metadata,
    Column("alternate_name_id", ForeignKey("alternate_names.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
dataset_distribution_relationship = Table(
    "dataset_distribution",
    Base.metadata,
    Column("distribution_id", ForeignKey("data_downloads.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
dataset_dataset_relationship = Table(
    "dataset_dataset",
    Base.metadata,
    Column("parent_id", ForeignKey("datasets.identifier")),
    Column("child_id", ForeignKey("datasets.identifier")),
)
dataset_keyword_relationship = Table(
    "dataset_keyword",
    Base.metadata,
    Column("keyword_id", ForeignKey("keywords.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
dataset_license_relationship = Table(
    "dataset_license",
    Base.metadata,
    Column("license_id", ForeignKey("licenses.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
dataset_publication_relationship = Table(
    "dataset_publication",
    Base.metadata,
    Column("publication_id", ForeignKey("publications.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
dataset_measuredValue_relationship = Table(
    "dataset_measuredValue",
    Base.metadata,
    Column("measuredValue_id", ForeignKey("measured_values.identifier")),
    Column("dataset_id", ForeignKey("datasets.identifier")),
)
