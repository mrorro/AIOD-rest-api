from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship
from database.model.named_relation import NamedRelation
from database.model.news.news_category_link import NewsCategoryNewsLink

if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.news import News


class NewsCategory(NamedRelation, table=True):  # type: ignore [call-arg]
    """
    News Categories or tags used to describe some item
    """

    __tablename__ = "news_category"

    news: List["News"] = Relationship(
        back_populates="news_categories", link_model=NewsCategoryNewsLink
    )
