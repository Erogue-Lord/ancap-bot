from decimal import Decimal
from datetime import datetime
import pytest


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch):
    global ancap_bot
    monkeypatch.delattr("dotenv.load_dotenv")
    import ancap_bot.cogs.economy


def test_salary():
    economy_cog = ancap_bot.cogs.economy.Economy(None)
    ancap_bot.db.updatedb()
    with ancap_bot.db.session_scope() as session:
        economy_cog.registrate(1, session)
        economy_cog.pay(datetime.now(), 1, session)
        user = ancap_bot.db.User.get_by_id(1, session)
        assert user.balance == 25
        session.delete(user)


def test_transference():
    economy_cog = ancap_bot.cogs.economy.Economy(None)
    ancap_bot.db.updatedb()
    with ancap_bot.db.session_scope() as session:
        economy_cog.registrate(1, session)
        economy_cog.registrate(2, session)
        user_1 = ancap_bot.db.User.get_by_id(1, session)
        user_2 = ancap_bot.db.User.get_by_id(2, session)
        user_1.balance += 20
        session.commit()
        ancap_bot.db.transaction(1, Decimal(10), 2)
        assert user_1.balance == 10
        assert user_2.balance == 10
        session.delete(user_1)
        session.delete(user_2)
