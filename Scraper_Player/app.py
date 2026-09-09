import sys
sys.dont_write_bytecode = True

import logging
from regulator.config import LoggingConfig
logging.basicConfig(
    filename=LoggingConfig.LOG_FILE, 
    encoding=LoggingConfig.LOG_ENCODING, 
    format=LoggingConfig.LOG_FORMAT,
    level=LoggingConfig.LOG_LEVEL, 
    datefmt=LoggingConfig.LOG_DATE_FMT
); logger = logging.getLogger(__name__)
import asyncio

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from graphic.frontend import MainWindow


def app_luncher() :

    app = QApplication(sys.argv)

    loop = QEventLoop(app) 
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__" :

    app_luncher()