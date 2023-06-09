from database.model.resource import Resource


class AIAsset(Resource):
    """
    Every database, publication, etc has relationship to the AIAsset.
    AIAsset inherets from Resource.
    class AIAsset only defines an entity of type AIAsset, however the relationship
    between ai_asset and an entity is defined in ai_asset_table.py.
    """

    pass
