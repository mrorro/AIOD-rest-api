import abc
import dataclasses
from typing import Any, TypeVar, Generic, Dict, List, Type

from fastapi import HTTPException
from pydantic.utils import GetterDict
from sqlmodel import SQLModel, Session, select

from database.model.named_relation import NamedRelation

MODEL = TypeVar("MODEL", bound=SQLModel)


class Serializer(abc.ABC, Generic[MODEL]):
    @abc.abstractmethod
    def serialize(self, model: MODEL) -> Any:
        pass


class DeSerializer(abc.ABC, Generic[MODEL]):
    @abc.abstractmethod
    def deserialize(self, session: Session, serialized: Any) -> MODEL | List[MODEL]:
        pass


class AttributeSerializer(Serializer):
    def __init__(self, attribute_name: str):
        self.attribute_name = attribute_name

    def serialize(self, model: MODEL) -> Any:
        return getattr(model, self.attribute_name)


def create_getter_dict(attribute_serializers: Dict[str, Serializer]):
    attribute_names = set(attribute_serializers.keys())

    class GetterDictSerializer(GetterDict):
        def get(self, key: Any, default: Any = None) -> Any:
            if key in attribute_names:
                attribute = getattr(self._obj, key)
                if attribute is not None:
                    serializer = attribute_serializers[key]
                    if isinstance(attribute, list):
                        return [serializer.serialize(v) for v in attribute]
                    return serializer.serialize(attribute)
            return super().get(key, default)

    return GetterDictSerializer


@dataclasses.dataclass
class FindByIdentifierDeserializer(DeSerializer[SQLModel]):
    clazz: type[SQLModel]

    def deserialize(self, session: Session, ids: list[int]) -> SQLModel | list[SQLModel]:
        if not isinstance(ids, list):
            raise ValueError("Expected list. This deserializer is not needed for single values.")
        query = select(self.clazz).where(self.clazz.identifier.in_(ids))  # noqa
        existing = session.scalars(query).all()
        ids_not_found = set(ids) - {e.identifier for e in existing}
        if any(ids_not_found):
            raise HTTPException(
                status_code=404,
                detail=f"Nested object with identifiers "
                f"{', '.join([str(i) for i in ids_not_found])} not found",
            )
        return sorted(existing, key=lambda o: o.identifier)


@dataclasses.dataclass
class FindByNameDeserializer(DeSerializer[NamedRelation]):
    clazz: type[NamedRelation]

    def deserialize(
        self, session: Session, name: str | list[str]
    ) -> NamedRelation | list[NamedRelation]:
        if not isinstance(name, list):
            query = select(self.clazz.identifier).where(self.clazz.name == name)
            identifier = session.scalars(query).first()
            if identifier is None:
                new_object = self.clazz(name=name)
                session.add(new_object)
                session.flush()
                identifier = new_object.identifier
            return identifier

        query = select(self.clazz).where(self.clazz.name.in_(name))  # type: ignore[attr-defined]
        existing = session.scalars(query).all()
        names_not_found = set(name) - {e.name for e in existing}
        new_objects = [self.clazz(name=name) for name in names_not_found]
        if any(names_not_found):
            session.add_all(new_objects)
            session.flush()
        return sorted(existing + new_objects, key=lambda o: o.identifier)


@dataclasses.dataclass
class CastDeserializer(DeSerializer[SQLModel]):
    clazz: type[SQLModel]

    def deserialize(self, session: Session, serialized: Any) -> SQLModel | List[SQLModel]:
        if not isinstance(serialized, list):
            return self._deserialize_single_resource(serialized, session)
        return [self._deserialize_single_resource(v, session) for v in serialized]

    def _deserialize_single_resource(self, serialized, session):
        resource = self.clazz.from_orm(serialized)
        update_resource_relationships(session, self.clazz, resource, serialized)
        return resource


def update_resource_relationships(
    session: Session,
    resource_class: Type[SQLModel],
    resource: SQLModel,
    resource_create_instance: SQLModel,
):
    if hasattr(resource_class, "RelationshipConfig"):
        relationships = {
            k: v
            for k, v in vars(resource_class.RelationshipConfig).items()
            if not k.startswith("_")
        }
        for attribute, relationship in relationships.items():
            new_value = getattr(resource_create_instance, attribute)
            if new_value is not None:
                if relationship.deserializer is not None:
                    deserialized = relationship.deserializer.deserialize(session, new_value)
                    setattr(resource, relationship.identifier_name or attribute, deserialized)
                else:
                    setattr(resource, relationship.identifier_name or attribute, new_value)
