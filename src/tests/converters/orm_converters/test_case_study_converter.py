import copy
import datetime

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from converters import case_study_converter_instance
from database.model.case_study import OrmCaseStudy
from database.model.dataset import OrmAlternateName
from database.model.general import OrmKeyword, OrmBusinessCategory, OrmTechnicalCategory
from database.model.publication import OrmPublication
from schemas import AIoDCaseStudy

CASE_STUDY_RELATION_FIELDS = (
    "alternate_names",
    "business_categories",
    "keywords",
    "technical_categories",
)


def test_aiod_to_orm_happy_path(
    engine: Engine,
    orm_case_study: OrmCaseStudy,
    aiod_case_study: AIoDCaseStudy,
    orm_publication: OrmPublication,
):

    aiod = copy.deepcopy(aiod_case_study)
    aiod.platform_identifier = "10"

    with Session(engine) as session:
        orm = case_study_converter_instance.aiod_to_orm(session, aiod)
        session.add(orm)
        session.commit()
        for field, expected_value in aiod.__dict__.items():
            if type(expected_value) is datetime.date:
                expected_value = datetime.datetime(
                    expected_value.year, expected_value.month, expected_value.day
                )
            if field not in CASE_STUDY_RELATION_FIELDS and field != "identifier":
                assert orm.__getattribute__(field) == expected_value, f"Error for field {field}"

        assert {a.name for a in orm.alternate_names} == set(aiod.alternate_names)
        assert {a.name for a in orm.business_categories} == set(aiod.business_categories)
        assert {a.name for a in orm.technical_categories} == set(aiod.technical_categories)
        assert {k.name for k in orm.keywords} == {"a", "b", "c"}
        assert all(
            {ds.identifier for ds in a.case_studies} == {orm.identifier}
            for a in orm.alternate_names
        )
        assert all(
            {ds.identifier for ds in a.case_studies} == {orm.identifier}
            for a in orm.business_categories
        )
        assert all(
            {ds.identifier for ds in a.case_studies} == {orm.identifier}
            for a in orm.technical_categories
        )
        assert all(
            {ds.identifier for ds in a.case_studies} == {orm.identifier} for a in orm.keywords
        )


def test_orm_to_aiod(orm_case_study: OrmCaseStudy):
    orm = copy.deepcopy(orm_case_study)
    orm.alternate_names = [OrmAlternateName(name="alias1"), OrmAlternateName(name="alias2")]
    orm.business_categories = [
        OrmBusinessCategory(name="business-cat1"),
        OrmBusinessCategory(name="business-cat2"),
    ]
    orm.keywords = [OrmKeyword(name="a"), OrmKeyword(name="b")]
    orm.technical_categories = [
        OrmTechnicalCategory(name="technical-cat1"),
        OrmTechnicalCategory(name="technical-cat2"),
    ]

    aiod = case_study_converter_instance.orm_to_aiod(orm)

    for field, actual_value in aiod.__dict__.items():
        if field not in CASE_STUDY_RELATION_FIELDS:
            expected_value = orm.__getattribute__(field)
            if (
                type(expected_value) is datetime.datetime
                and expected_value.time() == datetime.time.min
            ):
                expected_value = expected_value.date()
            assert actual_value == expected_value, f"Error for field {field}"
    assert aiod.alternate_names == ["alias1", "alias2"]
    assert aiod.business_categories == ["business-cat1", "business-cat2"]
    assert aiod.keywords == ["a", "b"]
    assert aiod.technical_categories == ["technical-cat1", "technical-cat2"]
