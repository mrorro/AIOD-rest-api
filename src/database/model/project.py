from datetime import datetime

from sqlalchemy import String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column

from database.model.ai_resource import OrmAIResource

from sqlalchemy import ForeignKey


class OrmProject(OrmAIResource):
    """Any project."""

    __tablename__ = "projects"

    identifier: Mapped[int] = mapped_column(
        ForeignKey("ai_resources.identifier"), init=False, primary_key=True
    )

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    doi: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=True, default=None)
    end_date: Mapped[datetime] = mapped_column(Date, nullable=True, default=None)
    founded_under: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    total_cost: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    eu_contribution: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    coordinated_by: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    project_description_title: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    project_description_text: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
    programmes_url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    topic_url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    call_for_proposal: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    foundung_scheme: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    # partners: Mapped[list[str]] = mapped_column(String(250), nullable=True, default=None)
    image: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)

    __mapper_args__ = {
        "polymorphic_identity": "project",
        "inherit_condition": identifier == OrmAIResource.identifier,
    }
