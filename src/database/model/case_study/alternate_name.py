from typing import List
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from database.model.named_relation import NamedRelation

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.case_study.case_study import CaseStudy


class CaseStudyAlternateNameLink(SQLModel, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_alternate_name_link"

    casestudy_identifier: int = Field(foreign_key="case_study.identifier", primary_key=True)
    alternate_name_identifier: int = Field(
        foreign_key="case_study_alternate_name.identifier", primary_key=True
    )


class CaseStudyAlternateName(NamedRelation, table=True):  # type: ignore [call-arg]
    __tablename__ = "case_study_alternate_name"

    case_studies: List["CaseStudy"] = Relationship(
        back_populates="alternate_names", link_model=CaseStudyAlternateNameLink
    )
