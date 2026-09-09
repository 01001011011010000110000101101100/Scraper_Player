import logging
import asyncio
from typing import Optional

import httpx
from httpx import URL

from regulator.config import InternetConfig


logger = logging.getLogger(__file__)


class NetworkManager:
    _client: Optional[httpx.AsyncClient] = None
    _semaphore: Optional[asyncio.Semaphore] = None

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        """ Create a client if not exists or uses the exist client and return it """
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(
                headers=InternetConfig.HEADERS,
                timeout=InternetConfig.TIMEOUT,
            )
        return cls._client

    @classmethod
    def get_semaphore(cls) -> asyncio.Semaphore:
        """ Lazy creating semaphore """
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(InternetConfig.MAX_CONCURRENT_REQUESTS)
        return cls._semaphore

    @classmethod
    async def close(cls):
        """ Close the client when the program is turn off """
        if cls._client and not cls._client.is_closed:
            await cls._client.aclose()


async def send_request(url: URL, follow: bool = False, retries: int = 3) -> httpx.Response | None:
    """Sends an asynchronous HTTP GET request with retries and rate-limit handling.

    1. Args:
        url (URL): Target `httpx.URL` object to request.
        follow (bool, optional): Whether to follow HTTP redirects. Defaults to `False`.
        retries (int, optional): Maximum retry attempts on failure/rate limit. Defaults to `3`.

    2. Returns:
        httpx.Response | None: The response object if status is `200`, otherwise `None`.

    3. Raises:
        TypeError: If `url` is not an instance of `httpx.URL` or `follow` is not a `bool`.
    """

    if not isinstance(url, URL) :
        logging.error(f"The parameter : {url} is not httpx.URL object")
        raise TypeError(f"Expected a httpx.URL instance, got {type(url).__name__}")

    if not isinstance(follow, bool) :
        logging.error(f"The parameter follow is not bool or the default value: {follow}")
        raise TypeError(f"Excepted a bool instance or the default value, got {type(follow).__name__}")

    client = NetworkManager.get_client()
    semaphore = NetworkManager.get_semaphore()

    for attempt in range(retries):
        async with semaphore :
            try:
                
                response = await client.get(
                    url=url,
                    follow_redirects=follow,
                    timeout=InternetConfig.TIMEOUT
                )

                logger.debug(f"Sended response to {url} waiting the response..")

                if not response:
                    logger.warning(f"Has no response from {url}")
                    await asyncio.sleep(InternetConfig.REQUEST_DELAY)
                    continue

                if response.status_code == 429:
                    logger.warning(f"Got temporary band from {url.host}")
                    wait_time = int(response.headers.get("Retry-After", 2 ** attempt))
                    await asyncio.sleep(wait_time)
                    continue

                if response.status_code != 200:
                    logger.warning(f"Has a response from {url} but the response is : {response.status_code}")
                    await asyncio.sleep(InternetConfig.REQUEST_DELAY)
                    continue

                logger.debug(f"Got valid response from {url}")
                return response
            
            except httpx.ConnectError:
                logger.error(f"Tried to request {url} without internet")
                print("Try to connect without an internet")
                return None

            except httpx.UnsupportedProtocol :
                logger.error(f"The URL : {url} have not protocol http or https")
                print("The URL without http/https protocol")
                return None

            except Exception as err:
                logger.error(f"An unexpected error occurred for {url}. More info: {err}")
                return None