import os
from decimal import Decimal

try:
    from dotenv import load_dotenv, find_dotenv
except ImportError:
    pass
else:
    load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")
DB = os.getenv("DB")
WAGE = Decimal(os.getenv("WAGE") or 25.00)
CHANNEL_PRICE = Decimal(os.getenv("CHANNEL_PRICE") or 100.00)
COOLDOWN = int(os.getenv("COOLDOWN") or 60)  # in seconds
CHANNEL_CATEGORY = os.getenv("CHANNEL_CATEGORY") or "Text Channels"
PREFIX = os.getenv("PREFIX") or "$"
LOCALE = os.getenv("LOCALE") or "en"
