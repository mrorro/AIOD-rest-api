from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.case_study.case_study import CaseStudy
from database.model.case_study.technical_category_link import CaseStudyTechnicalCategoryLink
from database.model.named_relation import NamedRelation


class TechnicalCategory(NamedRelation, table=True):  # type: ignore [call-arg]
    """
    Business Categories or tags used to describe some item
    """

    __tablename__ = "technical_category"

    case_studies: List["CaseStudy"] = Relationship(
        back_populates="technical_categories", link_model=CaseStudyTechnicalCategoryLink
    )
