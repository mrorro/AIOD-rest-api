import dataclasses
from typing import List, Type, Tuple, Any

from pydantic import create_model
from pydantic.utils import Representation
from sqlmodel import SQLModel, Field, UniqueConstraint
from sqlmodel.main import FieldInfo

from database.serialization import Serializer, create_getter_dict, DeSerializer
from platform_names import PlatformName


class Resource(SQLModel):
    platform: str = Field(default=None, schema_extra={"example": PlatformName.zenodo})
    platform_identifier: str = Field(default=None, schema_extra={"example": "1"})

    __table_args__ = (
        UniqueConstraint(
            "platform",
            "platform_identifier",
            name="resource_unique_platform_platform_identifier",
        ),
    )


def ResourceRelationship(*args, **kwargs) -> Any:
    return ResourceRelationshipInfo(*args, **kwargs)


@dataclasses.dataclass
class ResourceRelationshipInfo(Representation):
    serializer: Serializer | None = None
    deserializer: DeSerializer | None = None
    description: str | None = None
    example: str | List[str] | int | List[int] | None = None
    identifier_name: str | None = None

    def field(self):
        return Field(description=self.description, schema_extra={"example": self.example})


def get_relationships(resource_class: Type[SQLModel]) -> dict[str, ResourceRelationshipInfo]:
    if not hasattr(resource_class, "RelationshipConfig"):
        return {}

    return {
        k: v for k, v in vars(resource_class.RelationshipConfig).items() if not k.startswith("_")
    }


def get_field_definitions(
    resource_class: Type[Resource], relationships: dict[str, ResourceRelationshipInfo]
) -> dict[str, Tuple[Type, FieldInfo]]:
    if not hasattr(resource_class, "RelationshipConfig"):
        return {}
    return {
        attribute_name: (
            resource_class.RelationshipConfig.__annotations__[attribute_name],  # the type
            relationshipConfig.field(),  # The Field()
        )
        for attribute_name, relationshipConfig in relationships.items()
    }


def resource_create(resource_class: Type[Resource]) -> Type[SQLModel]:
    relationships = get_relationships(resource_class)
    field_definitions = get_field_definitions(resource_class, relationships)

    model = create_model(
        resource_class.__name__ + "Create", __base__=resource_class.__base__, **field_definitions
    )
    return model


def resource_read(resource_class: Type[Resource]) -> Type[SQLModel]:
    relationships = get_relationships(resource_class)
    field_definitions = get_field_definitions(resource_class, relationships)
    field_definitions.update({"identifier": (int, Field())})
    resource_class_read = create_model(
        resource_class.__name__ + "Read", __base__=resource_class.__base__, **field_definitions
    )
    update_model_serialization(resource_class, resource_class_read)
    relationships.items()
    return resource_class_read


def update_model_serialization(resource_class: Type[SQLModel], resource_class_read):
    relationships = get_relationships(resource_class)
    if hasattr(resource_class, "RelationshipConfig"):
        getter_dict = create_getter_dict(
            {
                attribute_name: relationshipConfig.serializer
                for attribute_name, relationshipConfig in relationships.items()
                if relationshipConfig.serializer is not None
            }
        )
        resource_class_read.__config__.getter_dict = getter_dict
