from decimal import Decimal

from .db import DataBase

def transaction(credentials, user, amount: Decimal, target=None):
    with DataBase(credentials) as db:
        db.cursor.execute(f'''
        select balance::money::numeric::float8 from users where user_id = {user}
        ''')
        balance = db.cursor.fetchall()
        if len(balance) == 0:
            raise ValueError("You're not registered, use $init to create your bank acount")
        balance = Decimal(balance[0][0])
        if balance >= amount:
            try:
                if target != None:
                    db.cursor.execute(f'''
                    select user_id from users where user_id = {target}
                    ''')
                    if len(db.cursor.fetchall()) == 0:
                        raise ValueError('Non-existent user')
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
                raise ValueError('Transaction failed')
        else:
            raise ValueError("You don't have that money")