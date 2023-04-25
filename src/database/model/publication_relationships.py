from sqlalchemy import Table, Column, ForeignKey

from database.model.base import Base

publication_license_relationship = Table(
    "publication_license",
    Base.metadata,
    Column("license_id", ForeignKey("licenses.identifier")),
    Column("publication_id", ForeignKey("publications.identifier")),
)
