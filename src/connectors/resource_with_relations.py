import dataclasses
from typing import TypeVar, Generic, List

from pydantic import BaseModel

AIOD_CLASS = TypeVar("AIOD_CLASS", bound=BaseModel)


@dataclasses.dataclass
class ResourceWithRelations(Generic[AIOD_CLASS]):
    resource: AIOD_CLASS
    related_resources: List[BaseModel] = dataclasses.field(default_factory=lambda: [])
