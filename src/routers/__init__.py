import typing  # noqa:F401 (flake8 raises incorrect 'Module imported but unused' error)

from .abstract_router import ResourceRouter  # noqa:F401
from .dataset_router import DatasetRouter
from .news_router import NewsRouter
from .publication_router import PublicationRouter
from .educational_resource_router import EducationalResourceRouter
from .event_router import EventRouter
from .organisation_router import OrganisationRouter

routers = [
    DatasetRouter(),
    PublicationRouter(),
    NewsRouter(),
    EducationalResourceRouter(),
    EventRouter(),
    OrganisationRouter(),
]  # type: typing.List[ResourceRouter]
