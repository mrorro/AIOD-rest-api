from typing import Iterator

from connectors import ResourceConnector
from connectors.example.utils import loadJsonData
from database.model.general.business_category import BusinessCategory
from database.model.general.keyword import Keyword
from database.model.general.media import Media
from database.model.general.news_category import NewsCategory
from database.model.news.news import News
from platform_names import PlatformName


class ExampleNewsConnector(ResourceConnector[News]):
    @property
    def platform_name(self) -> PlatformName:
        return PlatformName.example

    def fetch_all(self, limit: int | None = None) -> Iterator[News]:
        json_data = loadJsonData("news.json")

        news = [
            News(
                platform=item["platform"],
                platform_identifier=item["platform_identifier"],
                title=item["title"],
                date_modified=item["date_modified"],
                body=item["body"],
                section=item["section"],
                headline=item["headline"],
                word_count=item["word_count"],
                source=item["source"],
                alternative_headline=item["alternative_headline"],
                news_categories=[
                    NewsCategory(name=news_category) for news_category in item["news_categories"]
                ],
                media=[Media(name=media) for media in item["media"]],
                keywords=[Keyword(name=keyword) for keyword in item["keywords"]],
                business_categories=[
                    BusinessCategory(name=business_category)
                    for business_category in item["business_categories"]
                ],
            )
            for item in json_data
        ][:limit]

        yield from news

    def fetch(self, platform_identifier: str) -> News:
        (publication,) = [
            p for p in self.fetch_all(None) if p.resource.platform_identifier == platform_identifier
        ]
        return publication
