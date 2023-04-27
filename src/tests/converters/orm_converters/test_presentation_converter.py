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
