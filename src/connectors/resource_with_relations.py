import dataclasses
from typing import TypeVar, Generic, List

from sqlmodel import SQLModel

from database.model.resource import Resource

RESOURCE = TypeVar("RESOURCE", bound=SQLModel)


@dataclasses.dataclass
class ResourceWithRelations(Generic[RESOURCE]):
    """
    A resource, with related AIResources in a dictionary of {field_name: other resource(s)}.
    """

    resource: RESOURCE
    related_resources: dict[str, Resource | List[Resource]] = dataclasses.field(
        default_factory=dict
    )
    # For each field name, another resource or a list of other resources
