import os
from decimal import Decimal

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def sqlitepath():
    package_dir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.abspath(os.path.join(package_dir, "../db.sqlite"))
    return "".join(["sqlite:///", db_dir])


TOKEN = os.getenv("TOKEN")
DB = os.getenv("DB") or sqlitepath()
WAGE = Decimal(os.getenv("WAGE") or 25.00)
CHANNEL_PRICE = Decimal(os.getenv("CHANNEL_PRICE") or 100.00)
COOLDOWN = int(os.getenv("COOLDOWN") or 60)  # in seconds
CHANNEL_CATEGORY = os.getenv("CHANNEL_CATEGORY") or "Text Channels"
PREFIX = os.getenv("PREFIX") or "$"
LOCALE = os.getenv("LOCALE") or "en"
