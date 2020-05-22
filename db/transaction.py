from decimal import Decimal

from .db import DataBase

def transaction(credentials, user, amount: Decimal, target=None):
    with DataBase(credentials) as db:
        db.cursor.execute(f'''
        select balance::money::numeric::float8 from users where user_id = {user}
        ''')
        balance = db.cursor.fetchall()
        if len(balance) == 0:
            return 'Você nao está registrado, use $init para criar sua conta'
        balance = Decimal(balance[0][0])
        if balance >= amount:
            try:
                if target != None:
                    db.cursor.execute(f'''
                    select user_id from users where user_id = {target}
                    ''')
                    if len(db.cursor.fetchall()) == 0:
                        return 'Usuário inexistente'
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
                return 'Falha na transação'
            else:
                return 0
        else:
            return 'Você não tem esse dinheiro'