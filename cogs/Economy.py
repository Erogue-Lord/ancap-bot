import discord
from discord.ext import commands
import mysql.connector
from decimal import getcontext, Decimal
import configparser
from datetime import datetime  
from datetime import timedelta 

getcontext().prec = 3

class Economy(commands.Cog):
    def __init__(self, client):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.client = client
        self.conn = mysql.connector.connect(
            host=self.config['bot_db']['host'],
            user=self.config['bot_db']['user'],
            passwd=self.config['bot_db']['passwd'],
            database=self.config['bot_db']['database'],
        )
        self.cursor = self.conn.cursor()

    def registrate(self, id):
        self.cursor.execute(f'''
        INSERT into users (user_id)
        VALUES ({id});
        ''')
        self.conn.commit()

    def transaction(self, user, amount: Decimal, target=0):
        self.cursor.execute(f'''
        select balance from users where user_id = {user}
        ''')
        balance = self.cursor.fetchall()
        if len(balance) == 0:
            return 'Você nao está registrado, use $init para criar sua conta'
        balance = Decimal(balance[0][0])
        if balance >= amount:
            try:
                if target != 0:
                    self.cursor.execute(f'''
                    select user_id from users where user_id = {target}
                    ''')
                    if len(self.cursor.fetchall()) == 0:
                        return 'Usuário inexistente'
                    self.cursor.execute(f'''
                    UPDATE users
                    SET balance = balance + {amount}
                    WHERE user_id = {target}; 
                    ''')
                self.cursor.execute(f'''
                UPDATE users
                SET balance = balance - {amount}
                WHERE user_id = {user};
                ''')
            except:
                return 'Falha na transação'
            else:
                self.conn.commit()
                return 0
        else:
            return 'Você não tem esse dinheiro'

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.registrate(member.id)
        role = discord.utils.get(member.guild.roles, name='ancap')
        await member.add_roles(role)

    @commands.command()
    async def init(self, ctx):
        _id = ctx.author.id
        self.cursor.execute(f'''
        select user_id from users where user_id = {_id};
        ''')
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.registrate(_id)
            role = discord.utils.get(ctx.guild.roles, name='ancap')
            await ctx.author.add_roles(role)
            await ctx.send('Usuário registrado com sucesso!')
        else:
            await ctx.send('Você já está registrado')

    @commands.command()
    async def trabalhar(self, ctx):
        _id = ctx.author.id
        self.cursor.execute(f'''
        select work from users where user_id = {_id};
        ''')
        date = self.cursor.fetchall()[0][0]
        now = datetime.now()
        if date == None:
            self.cursor.execute(f'''
            UPDATE users
            SET 
                work = '{now}',
                balance = balance + 100
            WHERE
                user_id = {_id};
            ''')
            self.conn.commit()
            await ctx.send("Você ganhou AC$25.00")
        else:
            if date + timedelta(minutes=1) <= now:
                self.cursor.execute(f'''
                UPDATE users
                SET 
                    work = '{now}',
                    balance = balance + 100
                WHERE
                    user_id = {_id};
                ''')
                self.conn.commit()
                await ctx.send("Você ganhou AC$25.00")
            else:
                intervalo = (date + timedelta(minutes=1)) - now
                await ctx.send(f"Você tem que esperar {intervalo - timedelta(microseconds=intervalo.microseconds)} para trabalhar novamente")


    @commands.command()
    async def saldo(self, ctx):
        user_id = ctx.author.id
        self.cursor.execute(f'''
        select balance from users where user_id = {user_id}
        ''')
        try:
            balance = self.cursor.fetchall()[0][0]
        except:
            await ctx.send('Você não está registrado, use $init para criar sua conta bancária')
        else:
            await ctx.send(f'{ctx.author} tem AC${balance:.2f}')

    @commands.command(help='da dinheiro ao seu amiguinho')
    async def trans(self, ctx, amount: Decimal, user):
        target_id = int(user[3:-1])
        user_id = ctx.author.id
        server = ctx.guild
        result = self.transaction(user_id, amount, target_id)
        if result == 0:
            result = f'AC${amount:.2f} foram tranferidos para {server.get_member(target_id)}'
        await ctx.send(result)

    @commands.command()
    async def canal(self, ctx, *, name):
        def check(message):
            return message.author == ctx.message.author and (message.content == "s" or message.content == "n")
        await ctx.send('Você quer criar um canal? isso ira te custar AC$100[s/n]')
        msg = await self.client.wait_for('message', check=check, timeout=30)
        if msg.content == 's':
            result = self.transaction(ctx.message.author.id, 100.00)
            if result == 0:
                guild = ctx.guild
                name = name.replace(' ', '-')
                category = discord.utils.get(guild.categories, name='Canais de Texto')
                await guild.create_text_channel(name, category=category)
                channel = discord.utils.get(guild.channels, name=name)
                await channel.set_permissions(ctx.message.author, manage_permissions=True)
                await ctx.send(f'Canal {name} criado')
            else:
                await ctx.send(result)
        elif msg.content == 'n':
            await ctx.send('Operação cancelada') 

def setup(client):
    client.add_cog(Economy(client))