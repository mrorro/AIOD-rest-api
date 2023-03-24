import dataclasses
import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase, MappedAsDataclass):
    """Maps subclasses to Python Dataclasses, providing e.g., `__init__` automatically."""

    def to_dict(self, depth: int = 1) -> dict:
        """
        Serializes all fields of the dataclasses, as well as its references, up to a certain
        depth.

        Whenever the attributes are themselves dataclasses, such as Datasets referencing
        Publications, these dataclasses may refer back to other dataclasses, possibly in a cyclic
        manner. For this reason, using dataclasses.to_dict(object) results in infinite recursion.
        To prevent this from happening, we define this method which only recurs a `depth` amount
        of time.

        Params
        ------
        depth, int (default=1): dictates how many levels of object references to jsonify.
          When maximum depth is reached, any further references will simply be omitted.
          E.g., for depth=1 a Dataset will include Publications in its JSON, but not the
          Publications' Datasets.
        """
        d = {}  # type: typing.Dict[str, typing.Any]
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if isinstance(value, Base):
                if depth > 0:
                    d[field.name] = value.to_dict(depth=depth - 1)
            elif isinstance(value, (list, set)):
                if len(value) == 0:
                    pass
                elif all(isinstance(item, Base) for item in value):
                    if depth > 0:
                        d[field.name] = type(value)(item.to_dict(depth - 1) for item in value)
                elif not all(isinstance(item, type(next(iter(value)))) for item in value):
                    raise NotImplementedError("Serializing mixed-type lists is not supported.")
                else:
                    d[field.name] = value
            elif value is not None:
                d[field.name] = value
        return d


class BusinessCategory(Base):
    """Any business category"""

    __tablename__ = "business_categories"

    category: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class TechnicalCategory(Base):
    """Any business category"""

    __tablename__ = "technical_categories"

    category: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class Tag(Base):
    """Any tag"""

    __tablename__ = "tags"

    tag: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class TargetAudience(Base):
    __tablename__ = "target_audience"

    audience: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class Language(Base):
    __tablename__ = "languages"

    language: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
