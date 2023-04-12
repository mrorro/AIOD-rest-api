import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.organization_relationships import (
    organization_business_category_relationship,
    organization_technical_category_relationship,
    organization_organization_relationship,
)
from database.model.general import OrmBusinessCategory, OrmTechnicalCategory
from database.model.agent import OrmAgent, OrmEmail
from database.model.resource import OrmResource


class OrmOrganization(OrmResource, OrmAgent):
    """Any organization resource"""

    __tablename__ = "organizations"

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

    parent_organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.identifier"), nullable=True, default=None
    )

    subsidiary_organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.identifier"), nullable=True, default=None
    )

    business_categories: Mapped[list["OrmBusinessCategory"]] = relationship(
        secondary=organization_business_category_relationship,
        back_populates="organizations",
        passive_deletes=True,
        default_factory=list,
    )

    technical_categories: Mapped[list["OrmTechnicalCategory"]] = relationship(
        secondary=organization_technical_category_relationship,
        back_populates="organizations",
        passive_deletes=True,
        default_factory=list,
    )
    email_addresses: Mapped[list["OrmEmail"]] = relationship(
        cascade="all, delete-orphan",
        default_factory=list,
    )

    members: Mapped[list["OrmOrganization"]] = relationship(
        default_factory=list,
        back_populates="members",
        primaryjoin=organization_organization_relationship.c.parent_id == identifier,
        secondary=organization_organization_relationship,
        secondaryjoin=organization_organization_relationship.c.child_id == identifier,
    )
    departments: Mapped[list["OrmOrganization"]] = relationship(
        default_factory=list,
        back_populates="departments",
        primaryjoin=organization_organization_relationship.c.parent_id == identifier,
        secondary=organization_organization_relationship,
        secondaryjoin=organization_organization_relationship.c.child_id == identifier,
    )
