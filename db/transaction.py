from decimal import Decimal

from .db import (conn, cursor)

def transaction(user, amount: Decimal, target=None):
    cursor.execute(f'''
    select balance::money::numeric::float8 from users where user_id = {user}
    ''')
    balance = cursor.fetchall()
    if len(balance) == 0:
        return 'Você nao está registrado, use $init para criar sua conta'
    balance = Decimal(balance[0][0])
    if balance >= amount:
        try:
            if target != None:
                cursor.execute(f'''
                select user_id from users where user_id = {target}
                ''')
                if len(cursor.fetchall()) == 0:
                    return 'Usuário inexistente'
                cursor.execute(f'''
                UPDATE users
                SET balance = balance + {amount}
                WHERE user_id = {target}; 
                ''')
            cursor.execute(f'''
            UPDATE users
            SET balance = balance - {amount}
            WHERE user_id = {user};
            ''')
        except:
            return 'Falha na transação'
        else:
            conn.commit()
            return 0
    else:
        return 'Você não tem esse dinheiro'