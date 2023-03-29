import enum


class NodeName(str, enum.Enum):
    example = "example"
    openml = "openml"
    huggingface = "huggingface"
    zenodo = "zenodo"
