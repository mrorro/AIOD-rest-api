# from datetime import datetime
# from sqlalchemy.orm import Mapped, mapped_column
#
# from database.model.ai_resource import OrmAIResource
#
# from sqlalchemy import Boolean, Date, ForeignKey, String
#
#
# class OrmPresentation(OrmAIResource):
#     """Any presentation."""
#
#     __tablename__ = "presentations"
#
#     identifier: Mapped[int] = mapped_column(
#         ForeignKey("ai_resources.identifier"), init=False, primary_key=True
#     )
#
#     name: Mapped[str] = mapped_column(String(250), nullable=False)
#
#     author: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
#     description: Mapped[str] = mapped_column(String(500), nullable=True, default=None)
#     url: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
#     datePublished: Mapped[datetime] = mapped_column(Date, nullable=True, default=None)
#     publisher: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
#     image: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
#     is_accessible_for_free: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#
#     __mapper_args__ = {
#         "polymorphic_identity": "presentation",
#         "inherit_condition": identifier == OrmAIResource.identifier,
#     }
