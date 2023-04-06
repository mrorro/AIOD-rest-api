from database.model.resource import OrmResource
from sqlalchemy import UniqueConstraint
from database.model.event_relationships import event_ai_resource_relationship
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # avoid circular imports; only import while type checking
    from database.model.event import OrmEvent

class OrmAIResource(OrmResource):
    """The base class of all our AIResources such as Datasets, Publications etc..
    For now, it contains no fields, we will have to extend it later."""

    __tablename__ = "ai_resources"
    __table_args__ = (
        UniqueConstraint(
            "platform",
            "platform_identifier",
            name="ai_resource_unique_platform_platform_identifier",
        ),
    )

    # events: Mapped[list["OrmEvent"]] = relationship(
    #     default_factory=list,
    #     back_populates="ai_resources",
    #     secondary=event_ai_resource_relationship,
    # )    
    __mapper_args__ = {"polymorphic_identity": "ai_resource", "with_polymorphic": "*"}
   
    

