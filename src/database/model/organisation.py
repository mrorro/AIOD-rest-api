import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.organisation_relationships import (
    organisation_business_category_relationship,
    organisation_technical_category_relationship,
    organisation_organisation_relationship,
)
from database.model.general import OrmBusinessCategory, OrmTechnicalCategory
from database.model.agent import OrmAgent, OrmEmail
from database.model.resource import OrmResource


class OrmOrganisation(OrmResource, OrmAgent):
    """Any organisation resource"""

    __tablename__ = "organisations"

    identifier: Mapped[int] = mapped_column(init=False, primary_key=True)

    # required fields

    connection_to_ai: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(500), nullable=False)

    # optional fields
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    same_as: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    founding_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    dissolution_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    legal_name: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    alternate_name: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    address: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    telephone: Mapped[str] = mapped_column(String(500), nullable=True, default=None)

    parent_organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.identifier"), nullable=True, default=None
    )

    subsidiary_organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.identifier"), nullable=True, default=None
    )

    business_categories: Mapped[list["OrmBusinessCategory"]] = relationship(
        secondary=organisation_business_category_relationship,
        back_populates="organisations",
        passive_deletes=True,
        default_factory=list,
    )

    technical_categories: Mapped[list["OrmTechnicalCategory"]] = relationship(
        secondary=organisation_technical_category_relationship,
        back_populates="organisations",
        passive_deletes=True,
        default_factory=list,
    )
    email_addresses: Mapped[list["OrmEmail"]] = relationship(
        cascade="all, delete-orphan",
        default_factory=list,
    )

    members: Mapped[list["OrmOrganisation"]] = relationship(
        default_factory=list,
        back_populates="members",
        primaryjoin=organisation_organisation_relationship.c.parent_id == identifier,
        secondary=organisation_organisation_relationship,
        secondaryjoin=organisation_organisation_relationship.c.child_id == identifier,
    )
    departments: Mapped[list["OrmOrganisation"]] = relationship(
        default_factory=list,
        back_populates="departments",
        primaryjoin=organisation_organisation_relationship.c.parent_id == identifier,
        secondary=organisation_organisation_relationship,
        secondaryjoin=organisation_organisation_relationship.c.child_id == identifier,
    )
