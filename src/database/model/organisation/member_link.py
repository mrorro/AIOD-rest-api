from sqlmodel import SQLModel, Field


class OrganisationMemberLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_member_link"
    organisation_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)
    member_identifier: int = Field(foreign_key="agent_table.identifier", primary_key=True)
