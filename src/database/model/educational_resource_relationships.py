import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from sqlalchemy import ForeignKey, Table, Column

from database.model.base import Base

educational_resource_business_category_relationship = Table(
    "educational_resource_business_category",
    Base.metadata,
    Column(
        "educational_resource_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "business_category_id",
        ForeignKey("business_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

educational_resource_technical_category_relationship = Table(
    "educational_resource_technical_category",
    Base.metadata,
    Column(
        "educational_resource_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "technical_category_id",
        ForeignKey("technical_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

educational_resource_keyword_relationship = Table(
    "educational_resource_keyword",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "keyword_id",
        ForeignKey("keywords.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
)


educational_resource_target_audience_relationship = Table(
    "educational_resource_target_audience",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "target_audience_id",
        ForeignKey("target_audience.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
)


educational_resource_language_relationship = Table(
    "educational_resource_language",
    Base.metadata,
    Column(
        "educational_resrouce_id",
        ForeignKey("educational_resources.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "language_id",
        ForeignKey("languages.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True,
    ),
)
