__version__ = "0.3.0"
__author__ = "Erogue Lord"
__email__ = "debz1@protonmail.com"
__copyright__ = "Copyright 2020, Erogue Lord"
__license__ = "MIT"

import os
import gettext
import logging

from . import settings

try:
    import uvloop
except ImportError:
    pass
else:
    import asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s',
                    level=settings.LOGLEVEL,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=settings.LOGFILE)

if settings.LOCALE == "en":
    gettext.install("ancap_bot")
else:
    gettext.translation(
        "ancap_bot",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "locale")),
        languages=[settings.LOCALE],
    ).install()
