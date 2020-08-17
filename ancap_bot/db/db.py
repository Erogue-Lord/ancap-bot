import warnings
from contextlib import contextmanager
from decimal import Decimal
from typing import Optional

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from .. import _, settings
from . import models

engine = create_engine(settings.DB)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=exc.SAWarning)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def transaction(user_id: int, amount: Decimal, target_id: Optional[int] = None):
    with session_scope() as session:
        user = models.User.get_by_id(user_id, session)
        if user is None:
            raise ValueError(
                _("You're not registered, use $init to create your bank acount")
            )
        if user.balance >= amount:
            try:
                if target_id is not None:
                    target = models.User.get_by_id(target_id, session)
                    if target is None:
                        raise ValueError(_("Non-existent user"))
                    target.balance += amount
                user.balance -= amount
            except Exception:
                raise ValueError(_("Transaction failed"))
        else:
            raise ValueError(_("You don't have that money"))


def updatedb():
    models.Base.metadata.create_all(engine)
