from database.model.resource import OrmResource


class OrmAIResource(OrmResource):
    """The base class of all our AIResources such as Datasets, Publications etc..
    For now, it contains no fields, we will have to extend it later."""

    __abstract__ = True
