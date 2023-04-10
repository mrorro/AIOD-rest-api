import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from sqlalchemy import ForeignKey, Table, Column

from database.model.base import Base

organization_business_category_relationship = Table(
    "organization_business_category",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "business_category_id",
        ForeignKey("business_categories.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
)

organization_technical_category_relationship = Table(
    "organization_technical_category",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "technical_category_id",
        ForeignKey("technical_categories.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
)


organization_organization_relationship = Table(
    "organization_organization",
    Base.metadata,
    Column(
        "parent_id",
        ForeignKey("organizations.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "child_id",
        ForeignKey("ai_resources.identifier", ondelete="CASCADE"),
        primary_key=True,
    ),
)
