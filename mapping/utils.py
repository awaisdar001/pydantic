"""project utility methods"""

import re
from datetime import datetime
from typing import Optional

TAG_RE = re.compile(r'<[^>]+>')
PUB_DATE_FORMAT = '%Y-%m-%d-%H;%M;%S'
MOD_DATE_FORMAT = '%Y-%m-%d-%H:%M:%S'


def remove_tags(text: str) -> str:
    """Remove html from the text"""
    if TAG_RE.match(text):
        return TAG_RE.sub('', text)
    return text


def parse_published_date(str_date: str) -> Optional[datetime]:
    """Convert published date string to date object."""
    return to_datetime_object(str_date, PUB_DATE_FORMAT)


def parse_modified_date(str_date: str) -> Optional[datetime]:
    """Convert modified date string to date object."""
    return to_datetime_object(str_date, MOD_DATE_FORMAT)


def to_datetime_object(str_date: str, _format: str) -> Optional[datetime]:
    """Format & convert string date to date object with provided format."""
    return datetime.strptime(str_date, _format) if str_date else str_date
