__version__ = "0.2.1"
__author__ = "Erogue Lord"
__email__ = "debz1@protonmail.com"
__copyright__ = "Copyright 2020, Erogue Lord"
__license__ = "MIT"

import os
import gettext

from .bot import AncapBot
from . import settings

if settings.LOCALE == "en":
    gettext.install("ancap_bot")
else:
    gettext.translation(
        "ancap_bot",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "locale")),
        languages=[settings.LOCALE],
    ).install()

__all__ = ["AncapBot"]
