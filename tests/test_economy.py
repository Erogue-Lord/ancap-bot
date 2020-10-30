from decimal import Decimal
from contextlib import contextmanager
from datetime import datetime
import pytest


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch):
    global Economy, ancap_bot
    monkeypatch.delattr("dotenv.load_dotenv")
    import ancap_bot
    from ancap_bot.cogs.economy import Economy


@contextmanager
def create_user():
    economy_cog = Economy(None)
    ancap_bot.db.updatedb()
    with ancap_bot.db.session_scope() as session:
        economy_cog.registrate(1, session)
        yield session


def test_salary():
    with create_user() as session:
        economy_cog = Economy(None)
        economy_cog.pay(datetime.now(), 1, session)
        assert ancap_bot.db.User.get_by_id(1, session).balance == Decimal(25)
