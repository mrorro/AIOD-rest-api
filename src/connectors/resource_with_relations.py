import dataclasses
from typing import TypeVar, Generic, List

from pydantic import BaseModel

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=BaseModel)


@dataclasses.dataclass
class ResourceWithRelations(Generic[AIOD_CLASS]):
    resource: AIOD_CLASS
    related_resources: dict[str, BaseModel | List[BaseModel]] = dataclasses.field(
        default_factory=dict
    )
    # For each field name, another resource or a list of other resources
