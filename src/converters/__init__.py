from typing import Type  # noqa:F401

from schemas import AIoDDataset, AIoDNews, AIoDPublication, AIoDEducationalResource
from converters.orm_converters.abstract_converter import OrmConverter  # noqa:F401
from converters.orm_converters.dataset_converter import DatasetConverter
from converters.orm_converters.news_converter import NewsConverter
from converters.orm_converters.publication_converter import PublicationConverter
from converters.orm_converters.educational_resource_converter import EducationalResourceConverter

dataset_converter_instance = DatasetConverter()
news_converter_instance = NewsConverter()
publication_converter_instance = PublicationConverter()
educational_resource_converter_instance = EducationalResourceConverter()


converters = {
    AIoDDataset: dataset_converter_instance,
    AIoDEducationalResource: educational_resource_converter_instance,
    AIoDNews: news_converter_instance,
    AIoDPublication: publication_converter_instance,
}  # type: dict[Type, OrmConverter]
