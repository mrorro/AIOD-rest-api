from sqlmodel import SQLModel, Field


class OrganisationDepartmentLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "organisation_department_link"
    organisation_identifier: int = Field(foreign_key="organisation.identifier", primary_key=True)
    department_identifier: int = Field(foreign_key="agent_table.identifier", primary_key=True)
