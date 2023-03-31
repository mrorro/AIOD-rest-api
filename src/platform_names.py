import enum


class PlatformName(str, enum.Enum):
    """
    The platforms that are connected to AIoD, and AIoD itself. Every resource is part of a platform.

    TODO: move to a database table.
    """

    aiod = "aiod"
    example = "example"
    openml = "openml"
    huggingface = "huggingface"
    zenodo = "zenodo"
