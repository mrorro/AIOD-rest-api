"""
Contains the definitions for the different tables in our database.
See also:
   * https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column # noqa
   * https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses

Note: because we use MySQL in the demo, we need to explicitly set maximum string lengths.
"""
import dataclasses
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, String, UniqueConstraint, DateTime, Boolean, and_
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
    relationship,
)

from database.unique_model import UniqueMixin


class Base(DeclarativeBase, MappedAsDataclass):
    """Maps subclasses to Python Dataclasses, providing e.g., `__init__` automatically."""

    def to_dict(self, depth: int = 1) -> dict:
        """
        Serializes all fields of the dataclasses, as well as its references, up to a certain
        depth.

        Whenever the attributes are themselves dataclasses, such as Datasets referencing
        Publications, these dataclasses may refer back to other dataclasses, possibly in a cyclic
        manner. For this reason, using dataclasses.to_dict(object) results in infinite recursion.
        To prevent this from happening, we define this method which only recurs a `depth` amount
        of time.

        Params
        ------
        depth, int (default=1): dictates how many levels of object references to jsonify.
          When maximum depth is reached, any further references will simply be omitted.
          E.g., for depth=1 a Dataset will include Publications in its JSON, but not the
          Publications' Datasets.
        """
        d = {}  # type: typing.Dict[str, typing.Any]
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if isinstance(value, Base):
                if depth > 0:
                    d[field.name] = value.to_dict(depth=depth - 1)
            elif isinstance(value, (list, set)):
                if len(value) == 0:
                    pass
                elif all(isinstance(item, Base) for item in value):
                    if depth > 0:
                        d[field.name] = type(value)(item.to_dict(depth - 1) for item in value)
                elif not all(isinstance(item, type(next(iter(value)))) for item in value):
                    raise NotImplementedError("Serializing mixed-type lists is not supported.")
                else:
                    d[field.name] = value
            elif value is not None:
                d[field.name] = value
        return d


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


class DatasetDescription(Base):
    """Keeps track of which dataset is stored where."""

    __tablename__ = "datasets"
    __table_args__ = (
        UniqueConstraint(
            "node",
            "node_specific_identifier",
            name="dataset_unique_node_node_specific_identifier",
        ),
        UniqueConstraint(
            "node",
            "name",
            "version",
            name="dataset_unique_node_name_version",
        ),
    )

    # Required fields
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    description: Mapped[str] = mapped_column(String(5000), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    node: Mapped[str] = mapped_column(String(30), nullable=False)
    node_specific_identifier: Mapped[str] = mapped_column(String(250), nullable=False)
    same_as: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    # Recommended fields
    creator: Mapped[str] = mapped_column(String(150), default=None, nullable=True)
    # TODO(Jos): creator repeated organization/person
    date_modified: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    date_published: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    funder: Mapped[str] = mapped_column(String(150), default=None, nullable=True)
    # TODO(Jos): funder repeated organization/person
    is_accessible_for_free: Mapped[bool] = mapped_column(Boolean, default=None, nullable=True)
    issn: Mapped[str] = mapped_column(String(8), default=None, nullable=True)
    size: Mapped[int] = mapped_column(default=None, nullable=True)
    spatial_coverage: Mapped[str] = mapped_column(String(500), default=None, nullable=True)
    temporal_coverage_from: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    temporal_coverage_to: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    version: Mapped[str] = mapped_column(String(150), default=None, nullable=True)

    # Relations
    license: Mapped["License"] = relationship(
        back_populates="datasets", secondary=dataset_license_relationship, default=None
    )
    has_parts: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="is_part",
        primaryjoin=dataset_dataset_relationship.c.parent_id == id,
        secondary=dataset_dataset_relationship,
        secondaryjoin=dataset_dataset_relationship.c.child_id == id,
    )
    is_part: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="has_parts",
        primaryjoin=dataset_dataset_relationship.c.child_id == id,
        secondary=dataset_dataset_relationship,
        secondaryjoin=dataset_dataset_relationship.c.parent_id == id,
    )
    alternate_names: Mapped[list["AlternateName"]] = relationship(
        default_factory=list,
        back_populates="datasets",
        secondary=dataset_alternateName_relationship,
    )
    citations: Mapped[list["Publication"]] = relationship(
        default_factory=list,
        back_populates="datasets",
        secondary=dataset_publication_relationship,
    )
    distributions: Mapped[list["DataDownload"]] = relationship(
        default_factory=list,
        back_populates="dataset",
        secondary=dataset_distribution_relationship,
    )
    keywords: Mapped[list["Keyword"]] = relationship(
        default_factory=list,
        back_populates="datasets",
        secondary=dataset_keyword_relationship,
    )
    measured_values: Mapped[list["MeasuredValue"]] = relationship(
        default_factory=list,
        back_populates="datasets",
        secondary=dataset_measuredValue_relationship,
    )


class DataDownload(Base):
    """All or part of a Dataset in downloadable form"""

    __tablename__ = "data_downloads"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content_url: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    content_size_kb: Mapped[int] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(String(5000), default=None, nullable=True)
    encoding_format: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    name: Mapped[str] = mapped_column(String(150), default=None, nullable=True)
    dataset: Mapped["DatasetDescription"] = relationship(
        back_populates="distributions", secondary=dataset_distribution_relationship, init=False
    )


class AlternateName(UniqueMixin, Base):
    """An alias for an item"""

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "alternate_names"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    datasets: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="alternate_names",
        secondary=dataset_alternateName_relationship,
    )


class License(UniqueMixin, Base):
    """A license document that applies to this content, indicated by URL."""

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "licenses"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    datasets: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="license",
        secondary=dataset_license_relationship,
    )


class Keyword(UniqueMixin, Base):
    """Keywords or tags used to describe some item"""

    @classmethod
    def _unique_hash(cls, name):
        return name

    @classmethod
    def _unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    __tablename__ = "keywords"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    datasets: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="keywords",
        secondary=dataset_keyword_relationship,
    )


class MeasuredValue(UniqueMixin, Base):
    """The variable that this dataset measures. For example, temperature or pressure, including the
    technique, technology, or methodology used in a dataset"""

    @classmethod
    def _unique_hash(cls, variable, technique):
        return f"Variable:'{variable}'|Technique:'{technique}'"

    @classmethod
    def _unique_filter(cls, query, variable, technique):
        return query.filter(and_(cls.variable == variable, cls.technique == technique))

    __tablename__ = "measured_values"
    __table_args__ = (
        UniqueConstraint(
            "variable",
            "technique",
            name="measuredValue_variable_technique",
        ),
    )
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    variable: Mapped[str] = mapped_column(String(150))
    technique: Mapped[str] = mapped_column(String(150))
    datasets: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="measured_values",
        secondary=dataset_measuredValue_relationship,
    )


class Publication(Base):
    """Any publication."""

    __tablename__ = "publications"
    __table_args__ = (
        UniqueConstraint(
            "title",
            "url",
            name="publications_unique_title_url",
        ),
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    datasets: Mapped[list["DatasetDescription"]] = relationship(
        default_factory=list,
        back_populates="citations",
        secondary=dataset_publication_relationship,
    )
