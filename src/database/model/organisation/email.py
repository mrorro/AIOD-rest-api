from typing import List
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.organisation.organisation import Organisation


class OrganisationEmailLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_email_link"

    organisation_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)
    email_identifier: int = Field(foreign_key="organisation_email.identifier", primary_key=True)


class OrganisationEmail(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_email"

    organisations: List["Organisation"] = Relationship(
        back_populates="emails", link_model=OrganisationEmailLink
    )
