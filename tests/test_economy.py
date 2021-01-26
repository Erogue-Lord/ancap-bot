import asyncio
from datetime import datetime
from decimal import Decimal

from tortoise import Tortoise
import pytest


@pytest.fixture(autouse=True)
def event_loop(monkeypatch):
    global ancap_bot
    monkeypatch.delattr("dotenv.load_dotenv")
    import ancap_bot.cogs.economy
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ancap_bot.db.init())
    yield loop
    loop.run_until_complete(Tortoise.close_connections())
    loop.close()


def test_salary(event_loop):
    async def async_salary():
        await ancap_bot.db.init()
        economy_cog = ancap_bot.cogs.economy.Economy(None)
        await ancap_bot.db.User.create(user_id=1)
        await economy_cog.pay(datetime.now(), 1)
        user = await ancap_bot.db.User.filter(user_id=1).first()
        await user.save()
        assert user.balance == 25
        await Tortoise.close_connections()
    event_loop.run_until_complete(async_salary())


def test_transference(event_loop):
    async def async_transference():
        await ancap_bot.db.User.create(user_id=1)
        await ancap_bot.db.User.create(user_id=2)
        user_1 = await ancap_bot.db.User.filter(user_id=1).first()
        user_1.balance = 20
        await user_1.save()
        await ancap_bot.db.transaction(1, Decimal(10), 2)
        user_1 = await ancap_bot.db.User.filter(user_id=1).first()
        user_2 = await ancap_bot.db.User.filter(user_id=1).first()
        assert user_1.balance == 10
        assert user_2.balance == 10
    event_loop.run_until_complete(async_transference())
