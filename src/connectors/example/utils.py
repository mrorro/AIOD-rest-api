import json
import pathlib


def _path_example_resources() -> pathlib.Path:
    """Return the absolute path of src/tests/resources"""
    return pathlib.Path(__file__).parent / "resources"


def loadJsonData(file_name):
    with open(
        _path_example_resources() / file_name,
        "r",
    ) as f:
        return json.load(f)
