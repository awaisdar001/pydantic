"""sections data interface"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Union, List, Type

from utils import parse_published_date, parse_modified_date, remove_tags


class Parser(ABC):
    """Abstract base class for all article sections."""
    # A unique ID for the section.
    section_id: str = ''

    @classmethod
    @abstractmethod
    def get_section_data(cls, section_data) -> Dict[str, Union[str, int]]:
        """Parse & return section data."""


class SectionParser:
    """Base class for all sections."""

    @classmethod
    def _get_all_available_parsers(cls) -> List[Type[Parser]]:
        """Return all section parser classes available."""
        return Parser.__subclasses__()

    @classmethod
    def get(cls, section_type: str) -> Type[Parser]:
        """
        Get specific parser class of provided section type.
        """
        for parser in cls._get_all_available_parsers():
            if parser.section_id == section_type:
                return parser
        raise ValueError(f'Unknown "{section_type}" section.')


class TextParser(Parser, SectionParser):
    """Text section parser."""
    section_id: str = 'text'

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, str]:
        """Parse & return section data."""
        return {
            'type': cls.section_id,
            'text': remove_tags(section_data.get('text', ''))
            #     check if none is allowed in text.
        }


class TitleParser(Parser, SectionParser):
    """Title section parser."""
    section_id: str = 'title'

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, str]:
        """Parse & return section data."""
        return {
            'type': cls.section_id,
            'text': remove_tags(section_data['text'])
        }


class LeadParser(Parser, SectionParser):
    """Lead section parser."""
    section_id: str = ''

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, str]:
        """Parse & return section data."""
        return {
            'type': cls.section_id,
            'text': remove_tags(section_data['text'])
        }


class HeaderParser(Parser, SectionParser):
    """Header section parser."""
    section_id: str = 'header'

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, Union[str, int]]:
        """Parse & return section data."""
        return {
            'type': cls.section_id,
            'level': int(section_data['level']),
            'text': remove_tags(section_data['text']),
        }


class ImageParser(Parser, SectionParser):
    """Image section parser."""
    section_id: str = 'image'

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, str]:
        """Parse & return section data."""
        return {
            'type': cls.section_id,
            'url': section_data['url'],
            'alt': section_data.get('alt'),
            'caption': section_data.get('caption'),
            'source': section_data.get('source'),
        }


class MediaParser(Parser, SectionParser):
    """Media section parser."""
    section_id: str = 'media'

    @classmethod
    def get_section_data(cls, section_data) -> Dict[str, Union[str, datetime]]:
        """Parse & return section data."""
        media_data = {
            'type': cls.section_id,
            'id': section_data['id'],
            'url': section_data['url'],
            'thumbnail': section_data.get('thumbnail'),
            'caption': section_data.get('caption'),
            'author': section_data.get('author'),
            'publication_date': parse_published_date(section_data['pub_date']),
            'modification_date': parse_modified_date(section_data.get('mod_date')),
            'duration': section_data.get('duration'),
        }
        return media_data
