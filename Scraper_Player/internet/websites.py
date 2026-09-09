# websites.py
from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import re
from collections.abc import Callable

import httpx
from httpx import URL
from bs4 import BeautifulSoup

from internet.internet_handle import send_request
from regulator.models import IconModel, PageDetailsModel, EpisodeModel
from regulator.config import NotFoundDataConfig

logger = logging.getLogger(__file__)
patterns = {
    'title_pattern' : re.compile(r"[a-zA-Z][a-zA-Z0-9\s.:]+[a-zA-Z0-9]"),
    "m3u8_pattern" : re.compile(r'https?://[^\s"\'`]+\.m3u8[^\s"\'`]*'),
    'picture_pattern' : re.compile(r"url\(['\"]?(https?://[^'\"]+)['\"]?\)"),
}

class BaswParser(ABC):

    domain: URL

    @abstractmethod
    def parse_main_icons(self, soup: BeautifulSoup) -> List[IconModel | None]: ...
        
    @abstractmethod
    def parse_card_details(self, soup: BeautifulSoup) -> PageDetailsModel: ...

    @abstractmethod
    async def extract_sturl(self, source_url: URL) -> URL | None: ...

    @abstractmethod
    async def searcher(self, subject: str) -> List[IconModel | None]: ...

 
class WebsitesError(Exception):
    """Base exception for errors associated with BaswParser."""

class ParserClassNotFound(WebsitesError):
    """The parser of the website does not exist."""

class ParserFuncNotFound(WebsitesError):
   """The parser function for the page or icons does not exist."""



class WebsitesRegistry:
    """
    A registry of available website parsers.
    Each entry maps a website's base URL to its corresponding parser instance.
    """
    # Add more websites and their corresponding parser instances as needed
    registry: dict[URL, BaswParser] = {
    }

    @classmethod
    def gtpars(cls, url: URL) -> Optional[BaswParser] :
        """
            Takes httpx.URL instance and return the parser that associated with the URL.
            Accept full URL also it goes to extract the main domain.
        """
        base_url = URL(f"{url.scheme}://{url.host}/")
        return cls.registry.get(base_url)
 
    @classmethod
    def gtkeys(cls):
        """  Return the keys in registry. the key have httpx.URL instance. """
        return cls.registry.keys()

    @classmethod
    def gtsearchers(cls) -> List[Callable[[str], List[IconModel | None]]] :
        """ Returns all searcher functions that defined """
        searchers : List[Callable[[str], List[IconModel | None]]] = []
        for _, obj in cls.registry.items() :
            srch = obj.searcher
            if not srch :
                logger.error(f"Cannot found the searcher function of {type(obj).__name__}")
                raise ParserFuncNotFound(f"The searcher function of {type(obj).__name__} does not exist")

            searchers.append(srch)
        return searchers

# import httpx

# headers ={
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
#     'Referer': 'https://www.mp4upload.com/',
#     'Cookie': '_gid=GA1.2.1093092016.1787370570; _ga=GA1.2.724234754.1787370570;'
# }
# url = 'https://a4.mp4upload.com:183/d/xkx7yanoz3b4quuoaosboj2qjgnm4exbwjhqlpdgxbhebevm3nbw3qsjiltfy3oyc4tgnvpb/video.mp4'
# response = httpx.head(url, headers=headers, follow_redirects=True)
# if response.status_code == 200:
#     print("Yes")
# else :
#     print(response.status_code)