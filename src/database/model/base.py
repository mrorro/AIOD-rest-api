import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    """Maps subclasses to Python Dataclasses, providing e.g., `__init__` automatically."""

    pass
