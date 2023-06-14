from database.model.resource import Resource


class AIAsset(Resource):
    """ "
    Many resources, such as dataset and publication, are a type of AIAsset
    and should therefore inherit from this AIAsset class.
    Shared fields can be defined on this class.

    Notice the difference between AIAsset and AIAssetTable.
    The latter enables defining a relationship to "any AI Asset",
    by making sure that the identifiers of all resources that
    are AIAssets, are unique over the AIAssets.
    """
