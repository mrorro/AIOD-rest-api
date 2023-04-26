from sqlalchemy import Table, Column, ForeignKey

from database.model.base import Base

case_study_alternateName_relationship = Table(
    "case_study_alternateName",
    Base.metadata,
    Column("alternate_name_id", ForeignKey("alternate_names.identifier")),
    Column("case_study_id", ForeignKey("case_studies.identifier")),
)
case_study_business_category_relationship = Table(
    "case_study_business_category",
    Base.metadata,
    Column("case_study_id", ForeignKey("case_studies.identifier")),
    Column("business_category_id", ForeignKey("business_categories.identifier")),
)
case_study_keyword_relationship = Table(
    "case_study_keyword",
    Base.metadata,
    Column("keyword_id", ForeignKey("keywords.identifier")),
    Column("case_study_id", ForeignKey("case_studies.identifier")),
)
case_study_technical_category_relationship = Table(
    "case_study_technical_category",
    Base.metadata,
    Column("case_study_id", ForeignKey("case_studies.identifier")),
    Column("technical_category_id", ForeignKey("technical_categories.identifier")),
)
