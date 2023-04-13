from typing import Type  # noqa:F401

from schemas import AIoDDataset, AIoDNews, AIoDPublication, AIoDEducationalResource
from .orm_converters.abstract_converter import OrmConverter  # noqa:F401
from .orm_converters.dataset_converter import DatasetConverter
from .orm_converters.educational_resource_converter import EducationalResourceConverter
from .orm_converters.event_converter import EventResourceConverter
from .orm_converters.news_converter import NewsConverter
from .orm_converters.publication_converter import PublicationConverter

dataset_converter_instance = DatasetConverter()
news_converter_instance = NewsConverter()
publication_converter_instance = PublicationConverter()
educational_resource_converter_instance = EducationalResourceConverter()
event_converter_instance = EventResourceConverter()

converters = {
    AIoDDataset: dataset_converter_instance,
    AIoDEducationalResource: educational_resource_converter_instance,
    AIoDNews: news_converter_instance,
    AIoDPublication: publication_converter_instance,
}  # type: dict[Type, OrmConverter]
