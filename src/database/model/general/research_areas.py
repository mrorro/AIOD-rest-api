from typing import List
from typing import TYPE_CHECKING

from sqlmodel import Relationship
from database.model.event.research_area_link import EventResearchAreaLink


if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.event.event import Event
from database.model.named_relation import NamedRelation


class ResearchArea(NamedRelation, table=True):  # type: ignore [call-arg]
    """
    Research area used to describe some item
    """

    __tablename__ = "research_area"

    events: List["Event"] = Relationship(
        back_populates="research_areas", link_model=EventResearchAreaLink
    )
