"""
    Config file contain the config setting for several things (e.g., Logging, Internet...).
"""

import logging
import os

import httpx

from regulator.models import PageDetailsModel

class LoggingConfig:
    """
        The config setting object for logging system.
        Uses in the main file that run the program. 
    """
    LOG_FILE = os.getenv("LOG_FILE", os.path.join(os.path.dirname(os.path.abspath('__main__')), 'app.log'))
    LOG_LEVEL = logging.INFO 
    LOG_DATE_FMT = " %Y / %m / %d || %I : %M : %S %p"
    LOG_ENCODING = 'utf-8'
    LOG_FORMAT = (
        "Time => %(asctime)s, Logger => %(name)s, Level => %(levelname)s, File => %(filename)s \n "
        "Line => %(lineno)d, Function => %(funcName)s, Message : %(message)s \n"
    )


class InternetConfig:
    
    MAX_CONCURRENT_REQUESTS: int = 5 
    REQUEST_DELAY: float = 0.1
    HEADERS: httpx.Headers = httpx.Headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    TIMEOUT: httpx.Timeout = httpx.Timeout(connect=15.0, read=30.0, write=10.0, pool=10.0)


class NotFoundDataConfig:

    NO_PAGE_FOUND: PageDetailsModel = PageDetailsModel(title="Unknown", description="No data available")
