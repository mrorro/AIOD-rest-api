from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.dataset import Dataset
    from database.model.case_study.case_study import CaseStudy
from database.model.dataset.keyword_link import DatasetKeywordLink
from database.model.case_study.keyword_link import CaseStudyKeywordLink
from database.model.named_relation import NamedRelation


class Keyword(NamedRelation, table=True):  # type: ignore [call-arg]
    """
    Keywords or tags used to describe some item
    """

    __tablename__ = "keyword"

    datasets: List["Dataset"] = Relationship(
        back_populates="keywords", link_model=DatasetKeywordLink
    )

    case_studies: List["CaseStudy"] = Relationship(
        back_populates="keywords", link_model=CaseStudyKeywordLink
    )
