from sqlalchemy import Table, Column, ForeignKey

from database.model.base import Base


dataset_alternateName_relationship = Table(
    "dataset_alternateName",
    Base.metadata,
    Column("alternate_name_id", ForeignKey("alternate_names.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
dataset_distribution_relationship = Table(
    "dataset_distribution",
    Base.metadata,
    Column("distribution_id", ForeignKey("data_downloads.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
dataset_dataset_relationship = Table(
    "dataset_dataset",
    Base.metadata,
    Column("parent_id", ForeignKey("datasets.id")),
    Column("child_id", ForeignKey("datasets.id")),
)
dataset_keyword_relationship = Table(
    "dataset_keyword",
    Base.metadata,
    Column("keyword_id", ForeignKey("keywords.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
dataset_license_relationship = Table(
    "dataset_license",
    Base.metadata,
    Column("license_id", ForeignKey("licenses.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
dataset_publication_relationship = Table(
    "dataset_publication",
    Base.metadata,
    Column("publication_id", ForeignKey("publications.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
dataset_measuredValue_relationship = Table(
    "dataset_measuredValue",
    Base.metadata,
    Column("measuredValue_id", ForeignKey("measured_values.id")),
    Column("dataset_id", ForeignKey("datasets.id")),
)
