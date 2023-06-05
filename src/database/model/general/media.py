from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship


if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.news.news import News
from database.model.news.media_link import NewsMediaLink
from database.model.named_relation import NamedRelation


class Media(NamedRelation, table=True):  # type: ignore [call-arg]
    """
    Media
    """

    __tablename__ = "media"

    news: List["News"] = Relationship(back_populates="media", link_model=NewsMediaLink)
