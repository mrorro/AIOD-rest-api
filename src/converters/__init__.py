from typing import Type  # noqa:F401

from schemas import AIoDDataset, AIoDNews, AIoDPublication
from .abstract_converter import ResourceConverter  # noqa:F401
from .dataset_converter import DatasetConverter
from .news_converter import NewsConverter
from .publication_converter import PublicationConverter

dataset_converter_instance = DatasetConverter()
news_converter_instance = NewsConverter()
publication_converter_instance = PublicationConverter()


converters = {
    AIoDDataset: dataset_converter_instance,
    AIoDNews: news_converter_instance,
    AIoDPublication: publication_converter_instance,
}  # type: dict[Type, ResourceConverter]
