from typing import Type  # noqa:F401

from schemas import (
    AIoDDataset,
    AIoDEducationalResource,
    AIoDNews,
    AIoDPublication,
    AIoDProject,
    AIoDEvent,
    AIoDOrganisation,
    AIoDCaseStudy,
)
from .orm_converters.case_study_converter import CaseStudyConverter
from .orm_converters.organisation_converter import OrganisationResourceConverter

from .orm_converters.orm_converter import OrmConverter  # noqa:F401
from .orm_converters.dataset_converter import DatasetConverter
from .orm_converters.educational_resource_converter import EducationalResourceConverter
from .orm_converters.event_converter import EventResourceConverter
from .orm_converters.news_converter import NewsConverter
from .orm_converters.project_converter import ProjectConverter  # noqa:F401
from .orm_converters.publication_converter import PublicationConverter


case_study_converter_instance = CaseStudyConverter()
dataset_converter_instance = DatasetConverter()
news_converter_instance = NewsConverter()
publication_converter_instance = PublicationConverter()
project_converter_instance = ProjectConverter()
educational_resource_converter_instance = EducationalResourceConverter()
event_converter_instance = EventResourceConverter()
organisation_converter_instance = OrganisationResourceConverter()

converters = {
    AIoDCaseStudy: case_study_converter_instance,
    AIoDDataset: dataset_converter_instance,
    AIoDEducationalResource: educational_resource_converter_instance,
    AIoDNews: news_converter_instance,
    AIoDPublication: publication_converter_instance,
    AIoDProject: project_converter_instance,
    AIoDEvent: event_converter_instance,
    AIoDOrganisation: organisation_converter_instance,
}  # type: dict[Type, OrmConverter]
