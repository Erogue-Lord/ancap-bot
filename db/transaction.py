import gettext
from inspect import currentframe
import os

t = gettext.translation('base', "./locale", languages=[os.environ['locale']])

def _(s):
    frame = currentframe().f_back
    return eval(f"f'{t.gettext(s)}'", frame.f_locals, frame.f_globals)

from decimal import Decimal

from .db import DataBase

def transaction(user, amount, target=None):
    with DataBase() as db:
        db.cursor.execute(f'''
        select balance::money::numeric::float8 from users where user_id = {user}
        ''')
        balance = db.cursor.fetchall()
        if len(balance) == 0:
            raise ValueError(_("You're not registered, use $init to create your bank acount"))
        balance = Decimal(balance[0][0])
        if balance >= amount:
            try:
                if target != None:
                    db.cursor.execute(f'''
                    select user_id from users where user_id = {target}
                    ''')
                    if len(db.cursor.fetchall()) == 0:
                        raise ValueError(_("Non-existent user"))
                    db.cursor.execute(f'''
                    UPDATE users
                    SET balance = balance + {amount}
                    WHERE user_id = {target};
                    ''')
                db.cursor.execute(f'''
                UPDATE users
                SET balance = balance - {amount}
                WHERE user_id = {user};
                ''')
            except:
                raise ValueError(_("Transaction failed"))
        else:
            raise ValueError(_("You don't have that money"))