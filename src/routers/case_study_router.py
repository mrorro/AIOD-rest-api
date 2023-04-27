from typing import Type

from converters import dataset_converter_instance
from converters.orm_converters.orm_converter import OrmConverter
from database.model.case_study import OrmCaseStudy
from routers.resource_router import ResourceRouter
from schemas import AIoDCaseStudy


class CaseStudyRouter(ResourceRouter[OrmCaseStudy, AIoDCaseStudy]):
    @property
    def version(self) -> int:
        return 0

    @property
    def resource_name(self) -> str:
        return "case-study"

    @property
    def resource_name_plural(self) -> str:
        return "case-studies"

    @property
    def aiod_class(self) -> Type[AIoDCaseStudy]:
        return AIoDCaseStudy

    @property
    def orm_class(self) -> Type[OrmCaseStudy]:
        return OrmCaseStudy

    @property
    def converter(self) -> OrmConverter[AIoDCaseStudy, OrmCaseStudy]:
        return dataset_converter_instance
