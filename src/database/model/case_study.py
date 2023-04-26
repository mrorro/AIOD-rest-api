from datetime import datetime

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model.case_study_relationships import (
    case_study_alternateName_relationship,
    case_study_keyword_relationship,
    case_study_business_category_relationship,
    case_study_technical_category_relationship,
)
from database.model.dataset import OrmAlternateName
from database.model.general import OrmKeyword, OrmBusinessCategory, OrmTechnicalCategory
from database.model.resource import OrmResource


class OrmCaseStudy(OrmResource):
    """TODO: clear definition of Case Study, and why it's different from Project"""

    __tablename__ = "case_studies"

    # Required fields
    description: Mapped[str] = mapped_column(String(5000), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    # Recommended fields
    creator: Mapped[str] = mapped_column(String(150), default=None, nullable=True)
    publisher: Mapped[str] = mapped_column(String(150), default=None, nullable=True)
    # TODO(issue 9): contact + creator + publisher repeated organization/person
    date_modified: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    date_published: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    same_as: Mapped[str] = mapped_column(String(150), unique=True, default=None)
    url: Mapped[str] = mapped_column(String(150), unique=True, default=None)
    is_accessible_for_free: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relations
    alternate_names: Mapped[list["OrmAlternateName"]] = relationship(
        default_factory=list,
        back_populates="case_studies",
        secondary=case_study_alternateName_relationship,
    )
    business_categories: Mapped[list["OrmBusinessCategory"]] = relationship(
        default_factory=list,
        back_populates="case_studies",
        secondary=case_study_business_category_relationship,
    )
    keywords: Mapped[list["OrmKeyword"]] = relationship(
        default_factory=list,
        back_populates="case_studies",
        secondary=case_study_keyword_relationship,
    )
    technical_categories: Mapped[list["OrmTechnicalCategory"]] = relationship(
        default_factory=list,
        back_populates="case_studies",
        secondary=case_study_technical_category_relationship,
    )
