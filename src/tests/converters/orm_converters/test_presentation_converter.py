import datetime
from database.model.presentation import OrmPresentation
from schemas import AIoDPresentation
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import copy
from converters import presentation_converter_instance


def test_aiod_to_orm_happy_path(
    engine: Engine,
    orm_presentation: OrmPresentation,
    aiod_presentation: AIoDPresentation,
):

    aiod = copy.deepcopy(aiod_presentation)
    aiod.platform_identifier = "10"
    with Session(engine) as session:
        orm = presentation_converter_instance.aiod_to_orm(session, aiod)
        session.add(orm)
        session.commit()
        for field, expected_value in aiod.__dict__.items():
            if type(expected_value) is datetime.date:
                expected_value = datetime.datetime(
                    expected_value.year, expected_value.month, expected_value.day
                )


def test_orm_to_aiod(orm_presentation: OrmPresentation, aiod_presentation: AIoDPresentation):

    orm = copy.deepcopy(orm_presentation)

    aiod = presentation_converter_instance.orm_to_aiod(orm)

    for field, actual_value in aiod.__dict__.items():

        expected_value = orm.__getattribute__(field)
        if type(expected_value) is datetime.datetime and expected_value.time() == datetime.time.min:
            expected_value = expected_value.date()
        assert actual_value == expected_value, f"Error for field {field}"
