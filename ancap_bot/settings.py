import os
from decimal import Decimal

try:
    from dotenv import load_dotenv, find_dotenv
except ImportError:
    pass
else:
    load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")
DB = os.environ.get("DATABASE_URL", "sqlite:///:memory:")
WAGE = Decimal(os.environ.get("WAGE", 25.00))
CHANNEL_PRICE = Decimal(os.environ.get("CHANNEL_PRICE", 100.00))
COOLDOWN = int(os.environ.get("COOLDOWN", 60))  # in seconds
CHANNEL_CATEGORY = os.environ.get("CHANNEL_CATEGORY", "Text Channels")
PREFIX = os.environ.get("PREFIX", "$")
LOCALE = os.environ.get("LOCALE", "en")
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")
ROLE = os.environ.get("ROLE", "ancap")
LOGFILE = os.getenv("LOGFILE")
