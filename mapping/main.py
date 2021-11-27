"""scheduled python script to fetch & display articles."""
import json
import os
import re
import schedule
import time
from api import ArticleAPI
from models import Article
from pprint import pprint
from pydantic import ValidationError
from sections import SectionParser
from typing import Dict, Union, List, Optional
from urls import URLs
from utils import parse_published_date, parse_modified_date

TAG_RE = re.compile(r'<[^>]+>')
PUB_DATE_FORMAT = '%Y-%m-%d-%H;%M;%S'
MOD_DATE_FORMAT = '%Y-%m-%d-%H:%M:%S'

api = ArticleAPI()
DS = List[Dict[str, Union[str, int]]]


class ArticlesScript:
    """Article script."""

    articles: Dict = {}
    data_file: str = 'data.json'

    def add_article_media_info(self, article_id: str, sections: DS) -> None:
        """
        Fetches & updates data with media information from the API for the given article.
        """
        article_media_info = api.get_article_media(article_id=article_id)
        for media_info in article_media_info:
            for index, section in enumerate(sections):
                if not section['type'] == 'media':
                    continue
                if section['id'] == media_info['id']:
                    sections[index] = media_info
                    break

    def get_and_parse_sections_details(self, sections: DS, article_id: str) -> DS:
        """
        Parses article section data.

        Checks if sections include media sections then fetches media detail &
        parse/transform into presentable data.
        """
        has_media = any([section for section in sections if section['type'] == 'media'])
        if has_media:
            self.add_article_media_info(article_id, sections)

        clean_sections = []
        for section in sections:
            section_data = SectionParser.get(section['type']).get_section_data(section)
            clean_sections.append(section_data)
        return clean_sections

    def check_and_add_new_articles(self) -> None:
        """
        Check and add if new articles are available.

        Checks if new articles are available then adds them in the data struct. After processing,
        it saves the information in the file to release the data from the memory.
        """
        articles = api.get_articles()
        new_articles = {
            article['id']: article for article in articles if article['id'] not in self.articles
        }
        if not new_articles:
            print('No new articles found.')
            return

        print(f'===> Found {len(new_articles)} new articles. Fetching details...')
        self.articles.update(new_articles)
        self.add_article_details(new_articles)
        self.write_article_data_to_file()
        self.cleanup_in_memory_data()

    def add_article_details(self, articles: Dict) -> None:
        """
        Fetches details for the given articles from the API & updates the data struct.
        """
        for article_id in articles:
            article_detail = api.get_article_detail(article_id)

            raw_sections = article_detail['sections']
            modification_date = article_detail.get('mod_date')
            categories = article_detail.get('category')
            article_data = {
                'id': article_id,
                'original_language': article_detail['original_language'],
                'url': URLs.ArticleDetail.format(article_id=article_id),
                'thumbnail': article_detail.get('thumbnail'),
                'tags': list(set(article_detail.get('tags'))),
                'author': article_detail.get('author'),
                'publication_date': parse_published_date(article_detail['pub_date']),
                'sections': self.get_and_parse_sections_details(raw_sections, article_id)
            }
            if modification_date:
                article_data['modification_date'] = parse_modified_date(modification_date)
            if categories:
                article_data['categories'] = list({categories})

            self.articles[article_id] = article_data

    def print_articles(self) -> None:
        """Prints pydantic object if its valid otherwise prints error."""
        try:
            for article_row in self.read_json_file():
                article = Article(**article_row)
                pprint(article.dict())
        except ValidationError as error:
            pprint(error.json())

    def write_article_data_to_file(self) -> None:
        """
        Helper method to write data to json file.

        Json data is compiled as a whole, for such reason its required to
        load and add new data before saving.
        """
        existing_data = self.read_json_file()
        current_data = [article for article_id, article in self.articles.items()]
        if existing_data:
            current_data += existing_data
        with open(self.data_file, 'a') as outfile:
            json.dump(current_data, outfile, default=str)

    def read_json_file(self) -> Optional[List]:
        """
        If the json file exists then it reads the json file and returns the data,
        otherwise returns None.
        """
        if os.path.isfile(self.data_file):
            with open(self.data_file) as json_file:
                data = json.load(json_file)
                return data

    def cleanup_in_memory_data(self) -> None:
        """
        Cleans up data struct to remove the data content that is already saved in file,
        leaving just the keys for future reference.
        """
        self.articles = {article_id: {} for article_id in self.articles}

    def load_articles_from_file(self) -> None:
        """Loads the existing articles into a data struct."""
        existing_data = self.read_json_file()
        if existing_data:
            self.articles = {article_row['id']: {} for article_row in existing_data}

    def run(self) -> None:
        """
        Public method to run script.
        """
        self.load_articles_from_file()
        self.check_and_add_new_articles()
        self.print_articles()


if __name__ == "__main__":
    # When the main script runs, run the script immediately.
    ArticlesScript().run()

    # Schedule task after every 5 mints
    schedule.every(5).minutes.do(ArticlesScript().run)
    while True:
        schedule.run_pending()
        time.sleep(1)
