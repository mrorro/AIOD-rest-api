import dataclasses
from typing import TypeVar, Generic, List

from schemas import AIoDAIResource, AIoDResource

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=AIoDResource)


@dataclasses.dataclass
class ResourceWithRelations(Generic[AIOD_CLASS]):
    """
    A resource, with related AIResources in a dictionary of {field_name: other resource(s)}.
    """

    resource: AIOD_CLASS
    related_resources: dict[str, AIoDAIResource | List[AIoDAIResource]] = dataclasses.field(
        default_factory=dict
    )
    # For each field name, another resource or a list of other resources
