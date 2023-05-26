# from typing import Iterator
#
# from connectors import ResourceConnector
# from platform_names import PlatformName
# from schemas import AIoDPublication
#
#
# class ExamplePublicationConnector(ResourceConnector[AIoDPublication]):
#     @property
#     def platform_name(self) -> PlatformName:
#         return PlatformName.example
#
#     def fetch_all(self, limit: int | None = None) -> Iterator[AIoDPublication]:
#         yield from [
#             AIoDPublication(
#                 title="AMLB: an AutoML Benchmark",
#                 url="https://arxiv.org/abs/2207.12560",
#                 doi="1",
#                 platform="example",
#                 platform_identifier="1",
#             ),
#             AIoDPublication(
#                 title="Searching for exotic particles in high-energy physics with deep learning",
#                 doi="2",
#                 platform="example",
#                 platform_identifier="2",
#             ),
#         ][:limit]
#
#     def fetch(self, platform_identifier: str) -> AIoDPublication:
#         return AIoDPublication(
#             doi="10.5281/zenodo.7712947",
#             title="International Journal of Current Science Research and Review",
#         )
