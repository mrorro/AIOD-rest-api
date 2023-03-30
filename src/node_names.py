import enum


class NodeName(str, enum.Enum):
    aiod = "aiod"
    example = "example"
    openml = "openml"
    huggingface = "huggingface"
    zenodo = "zenodo"
