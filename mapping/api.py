"""external api interface."""
from typing import Union, List, Dict

import requests

from urls import URLs

Response = requests.models.Response
RD = Union[List, Dict]


class ArticleAPI:
    """External articles data api."""

    def _response_data(self, response: Response) -> RD:
        """Internal method to return safely parse data when available."""
        if response.status_code == 200:
            return response.json()
        return []

    def get_articles(self) -> RD:
        """Fetches available article list."""
        articles_response = requests.get(URLs.ArticleList)
        return self._response_data(articles_response)

    def get_article_detail(self, article_id: str) -> RD:
        """Fetches details of provided article id."""
        article_detail_response = requests.get(URLs.ArticleDetail.format(article_id=article_id))
        return self._response_data(article_detail_response)

    def get_article_media(self, article_id: str) -> RD:
        """Fetches media information for provided article."""
        media_response = requests.get(URLs.ArticleMedia.format(article_id=article_id))
        return self._response_data(media_response)


article_api = ArticleAPI()
