import re
import logging
import os
import asyncio 

from typing import List, Set

import httpx
from bs4 import BeautifulSoup

from regulator.models import IconModel, PageDetailsModel, EpisodeModel
from internet.internet_handle import send_request
import internet.websites as webs
from regulator.config import NotFoundDataConfig

logger = logging.getLogger(__name__)


async def fetch_main_icons() -> List[IconModel | None]:
    """ 
        Fetches main icons from all registered websites.
        Returns a list of IconModel instances or None for each icon.
    """
    try:

        all_icons_data : List[IconModel | None] = []
        seen_title : Set[str] = set()
        frequenter_icons : List[IconModel | None] = []

        logger.info("Start fetching icons")

        tasks = [send_request(url) for url in webs.WebsitesRegistry.gtkeys()]
        responses = await asyncio.gather(*tasks)
        for res in responses:

            if not res :
                logger.warning(f"Did not get response from {res}")
                continue

            url = httpx.URL(res.url)
            suits_obj : webs.BaswParser = webs.WebsitesRegistry.gtpars(url)

            if not suits_obj:
                logger.error(f"No parser configured for domain: {url}")
                raise webs.ParserClassNotFound(f"The parser class for : {url} ")

            if not suits_obj.parse_main_icons :
                logger.error(f"The main icons parser function for :{url} Does not exist")
                raise webs.ParserFuncNotFound(f"There is no parse main icons function for {url}")

            main_icon_data = suits_obj.parse_main_icons(
                soup=BeautifulSoup(res.content, 'lxml')
            )
        
            for icon in main_icon_data:

                title = icon.title
                if title in seen_title :
                    frequenter_icons.append(icon)
                    continue

                seen_title.add(title)
                all_icons_data.append(icon)

                """
                    Compression Block. Later
                """

        return all_icons_data

    except (webs.WebsitesError):
        raise

    except Exception as err:
        logger.error(f"Unexpected error occurred while fetching main icons: {err}")
        raise RuntimeError("Failed to fetch main icons due to unexpected error") from err


async def fetch_card_data(page_url: httpx.URL) -> PageDetailsModel:
    """
    Takes a `httpx.URL` instance as page_url and pass to `scraper.send_request()` and by the returned values crete and return `PageDetailsModel` object.

    Parameters :
    * `page_url` -- httpx.`httpx.URL` instance of the target page.

    Returns :
    * `PageDetailsModel` -- using the returned value and create the object.
    """
    
    if not isinstance(page_url, httpx.URL):
        logger.error(f"The parameter: {page_url} is not a httpx.`httpx.URL` object")
        raise TypeError(f"Expected a httpx.`httpx.URL` instance, got {type(page_url).__name__}")

    try:

        logger.info(f"Start fetching page data of {page_url}")
        response = await send_request(page_url)
        
        if not response:
            logger.warning(f"No response received from {page_url}")
            return NotFoundDataConfig.NO_PAGE_FOUND

        parser_object : webs.BaswParser = webs.WebsitesRegistry.gtpars(page_url)

        if not parser_object:
            logger.error(f"No parser configured for card domain: {page_url.host}")
            raise webs.ParserClassNotFound(f"No parser available for domain {page_url.host}")

        if not parser_object.parse_card_details:
            logger.error(f"Cannot found the `parse_card_details` function for the domain {page_url.host}")
            raise webs.ParserFuncNotFound(f"The parser function for this domain: {page_url.host} does not exist or defined")

        return parser_object.parse_card_details(BeautifulSoup(response.content, 'lxml'))

    except (webs.WebsitesError, TypeError):
        raise

    except Exception as err:
        logger.exception(f"Unexpected error occurred while fetching {page_url}")
        raise RuntimeError(f"Failed to fetch card data for {page_url}") from err


async def fetch_stream_url(source_url: httpx.URL) -> httpx.URL | None :
    """ 
        Takes the site watch `httpx.URL` of the episode and returns the a 
    """
    if not isinstance(source_url, httpx.URL) :
        logger.error(f"Excepted httpx.`httpx.URL` instance as a parameter to fetch the watch url; however, got {type(source_url).__name__}")
        raise ValueError(f"Excepted httpx.`httpx.URL` instance, got {type(source_url).__name__}")
    
    try :

        par_obj : webs.BaswParser = webs.WebsitesRegistry.gtpars(source_url)
        
        if not par_obj:
            logger.error(f"Cannot found the parser object for this domain : {source_url.host}")
            raise webs.ParserFuncNotFound(f"No parser available for domain {source_url.host}")

        if not par_obj.extract_sturl :
            logger.error(f"Cannot found the `extract_sturl` function for the domain {source_url.host}")
            raise webs.ParserFuncNotFound(f"The parser function for this domain: {source_url.host} does not exist or defined")

        watch_data : httpx.URL | None = await par_obj.extract_sturl(source_url)
        return watch_data
    
    except (ValueError, webs.WebsitesError):
        raise

    except Exception as err:
        logger.error(f"Unexpected error occurred while extract source data of {source_url}. More info: {err}")
        raise RuntimeError(f"Unexpected error occurred while extract watch data of {source_url}.") from err


async def search(subject: str) -> List[IconModel | None] :

    try :

        cards_data : List[IconModel | None] = []
        seen_titles = set()

        for searcher in webs.WebsitesRegistry.gtsearchers() :
            result = await searcher(subject)
            cards_data.extend(result)

        return cards_data
    
    except Exception as err :
        logger.error(f"Unexpected error occurred while searching for {subject}. At {err}")
        raise RuntimeError("Unexpected error occurred") from err