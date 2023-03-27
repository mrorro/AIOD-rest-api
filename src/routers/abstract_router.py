import abc
import traceback
from typing import Generic, TypeVar, Type, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Engine, select, and_, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from connectors import NodeName
from database.model.base import Base


class Pagination(BaseModel):
    offset: int = 0
    limit: int = 100


ORM_CLASS = TypeVar("ORM_CLASS", bound=Base)
AIOD_CLASS = TypeVar("AIOD_CLASS", bound=BaseModel)


class ResourceRouter(abc.ABC, Generic[ORM_CLASS, AIOD_CLASS]):
    @property
    @abc.abstractmethod
    def resource_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def resource_name_plural(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def converter(self):
        pass

    @property
    @abc.abstractmethod
    def aiod_class(self) -> Type[AIOD_CLASS]:
        pass

    @property
    @abc.abstractmethod
    def orm_class(self) -> Type[ORM_CLASS]:
        pass

    def add_routes(self, engine: Engine, url_prefix: str):
        router = APIRouter()

        router.add_api_route(
            path=url_prefix + f"/{self.resource_name_plural}/",
            endpoint=self.list_resources_func(engine),
            response_model=List[self.aiod_class],  # type: ignore
            response_model_exclude_none=True,
            name=f"List {self.resource_name_plural}",
        )
        router.add_api_route(
            path=url_prefix + f"/nodes/{{node}}/{self.resource_name_plural}",
            endpoint=self.list_node_resources_func(engine),
            response_model=List[self.aiod_class],  # type: ignore
            response_model_exclude_none=True,
            name=f"List {self.resource_name_plural}",
        )

        router.add_api_route(
            path=url_prefix + f"/{self.resource_name_plural}/{{identifier}}",
            endpoint=self.get_resource_func(engine),
            response_model=self.aiod_class,  # type: ignore
            response_model_exclude_none=True,
            name=self.resource_name,
        )
        router.add_api_route(
            path=url_prefix + f"/nodes/{{node}}/{self.resource_name_plural}/{{identifier}}",
            endpoint=self.get_node_resource_func(engine),
            response_model=self.aiod_class,  # type: ignore
            response_model_exclude_none=True,
            name=self.resource_name,
        )
        router.add_api_route(
            path=url_prefix + f"/{self.resource_name_plural}/",
            methods={"POST"},
            endpoint=self.register_resource_func(engine),
            response_model=self.aiod_class,  # type: ignore
            response_model_exclude_none=True,
            name=self.resource_name,
        )
        router.add_api_route(
            path=url_prefix + f"/{self.resource_name_plural}/{{identifier}}",
            methods={"PUT"},
            endpoint=self.put_resource_func(engine),
            response_model=self.aiod_class,  # type: ignore
            response_model_exclude_none=True,
            name=self.resource_name,
        )
        router.add_api_route(
            path=f"{url_prefix}/{self.resource_name_plural}/{{identifier}}",
            methods={"DELETE"},
            endpoint=self.delete_resource_func(engine),
            name=self.resource_name,
        )
        return router

    def list_resources_func(self, engine: Engine):
        def list_resources(pagination: Pagination = Depends(Pagination)):
            f"""
            Lists all {self.resource_name_plural} registered with AIoD.

            Query Parameter
            ------
             * nodes, list[str], optional: if provided, list only resources from the given node.
            """
            try:
                with Session(engine) as session:
                    query = select(self.orm_class).offset(pagination.offset).limit(pagination.limit)
                    return [
                        self.converter.orm_to_aiod(dataset)
                        for dataset in session.scalars(query).all()
                    ]
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return list_resources

    def list_node_resources_func(self, engine: Engine):
        def list_resources(node: str, pagination: Pagination = Depends(Pagination)):
            f"""Retrieve all meta-data of the {self.resource_name_plural} of a single node."""
            try:
                with Session(engine) as session:
                    query = (
                        select(self.orm_class)
                        .where(self.orm_class.node == node)
                        .offset(pagination.offset)
                        .limit(pagination.limit)
                    )
                    return [
                        self.converter.orm_to_aiod(dataset)
                        for dataset in session.scalars(query).all()
                    ]
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return list_resources

    def get_resource_func(self, engine: Engine):
        def get_resource(identifier: str):
            f"""Retrieve all meta-data for a specific {self.resource_name}."""
            try:
                with Session(engine) as session:
                    dataset = self._retrieve_resource(session, identifier)
                    return self.converter.orm_to_aiod(dataset)
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return get_resource

    def get_node_resource_func(self, engine: Engine):
        def get_resource(node: str, identifier: str):
            f"""Retrieve all meta-data for a specific {self.resource_name} identified by the
            node-specific-identifier."""
            try:
                with Session(engine) as session:
                    dataset = self._retrieve_resource(session, identifier, node=node)
                    return self.converter.orm_to_aiod(dataset)
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return get_resource

    def register_resource_func(self, engine: Engine):
        clz = self.aiod_class

        def register_resource(resource: clz):  # type: ignore
            f"""Register a {self.resource_name} with AIoD."""
            try:
                with Session(engine) as session:
                    dataset_orm = self.converter.aiod_to_orm(session, resource)
                    session.add(dataset_orm)
                    try:
                        session.commit()
                    except IntegrityError:
                        session.rollback()
                        query = select(self.orm_class).where(
                            and_(
                                self.orm_class.node == resource.node,  # type: ignore
                                self.orm_class.node_specific_identifier  # type: ignore
                                == resource.node_specific_identifier,  # type: ignore
                            )
                        )
                        # TODO: removing the these type: ignores, by letting the ORM classes inherit
                        # from a class that contains node and node_specific_identifier (e.g.
                        # AiResource).
                        existing_resource = session.scalars(query).first()
                        raise HTTPException(
                            status_code=409,
                            detail=f"There already exists a {self.resource_name} with the same "
                            f"node and name, with id={existing_resource.id}.",
                        )
                    return self.converter.orm_to_aiod(dataset_orm)
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return register_resource

    def put_resource_func(self, engine: Engine):
        clz = self.aiod_class

        def put_resource(identifier: str, resource: clz):  # type: ignore
            f"""Update an existing {self.resource_name}."""
            try:
                with Session(engine) as session:
                    self._retrieve_resource(session, identifier)  # Raise error if it does not exist
                    dataset_orm = self.converter.aiod_to_orm(session, resource)
                    dataset_orm.id = identifier
                    session.merge(dataset_orm)
                    session.commit()
                    new_dataset = self._retrieve_resource(session, identifier)
                    return self.converter.orm_to_aiod(new_dataset)
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return put_resource

    def delete_resource_func(self, engine: Engine):
        def delete_resource(identifier: str):
            try:
                with Session(engine) as session:
                    self._retrieve_resource(session, identifier)  # Raise error if it does not exist
                    statement = delete(self.orm_class).where(self.orm_class.id == identifier)
                    session.execute(statement)
                    session.commit()
            except Exception as e:
                raise _wrap_as_http_exception(e)

        return delete_resource

    def _retrieve_resource(self, session, identifier, node=None):
        if node is None:
            query = select(self.orm_class).where(self.orm_class.id == identifier)
        else:
            if node not in {n.name for n in NodeName}:
                raise HTTPException(status_code=400, detail=f"Node '{node}' not recognized.")
            query = select(self.orm_class).where(
                and_(
                    self.orm_class.node_specific_identifier == identifier,
                    self.orm_class.node == node,
                )
            )
        dataset = session.scalars(query).first()
        if not dataset:
            if node is None:
                msg = f"{self.resource_name.capitalize()} '{identifier}' not found in the database."
            else:
                msg = (
                    f"{self.resource_name.capitalize()} '{identifier}' of '{node}' not found in "
                    "the database."
                )
            raise HTTPException(status_code=404, detail=msg)
        return dataset


def _wrap_as_http_exception(exception: Exception) -> HTTPException:
    if isinstance(exception, HTTPException):
        return exception

    # This is an unexpected error. A mistake on our part. End users should not be informed about
    # details of problems they are not expected to fix, so we give a generic response and log the
    # error.
    traceback.print_exc()
    return HTTPException(
        status_code=500,
        detail=(
            "Unexpected exception while processing your request. Please contact the maintainers."
        ),
    )
