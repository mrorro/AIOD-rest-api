import typing  # noqa:F401


from .abstract_router import ResourceRouter  # noqa:F401
from .dataset_router_v0 import DatasetRouterV0
from .news_router_v0 import NewsRouterV0
from .publication_router_v0 import PublicationRouterV0
from .educational_resource_router_v0 import EducationalResourceRouterV0
from .event_router_v0 import EventRouterV0
from .project_router_v0 import ProjectRouterV0

routers = [
    DatasetRouterV0(),
    PublicationRouterV0(),
    NewsRouterV0(),
    EducationalResourceRouterV0(),
    EventRouterV0(),
    ProjectRouterV0(),
]  # type: typing.List[ResourceRouter]
