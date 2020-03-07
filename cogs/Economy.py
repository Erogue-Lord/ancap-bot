import discord
from discord.ext import commands
import sqlite3
from decimal import getcontext, Decimal
#from discord.utils import *

getcontext().prec = 3

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

    def registrate(self, id):
        self.cursor.execute(f'''
        INSERT into users (user_id, balance)
        VALUES ({id}, 0.0);
        ''')
        self.conn.commit()

    def transaction(self, user, amount: Decimal, target=0):
        self.cursor.execute(f'''
        select balance from users where user_id = {user}
        ''')
        balance = Decimal(self.cursor.fetchall()[0][0])
        if balance >= amount:
            try:
                self.cursor.execute(f'''
                UPDATE users
                SET balance = balance - {amount}
                WHERE user_id = {user};
                ''')
                if target != 0:
                    self.cursor.execute(f'''
                    UPDATE users
                    SET balance = balance + {amount}
                    WHERE user_id = {target}; 
                    ''')
                self.conn.commit()
            except:
                return 'Falha na transação'
            else:
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
            try:
                self.registrate(_id)
            except:
                await ctx.send('Falha no registro')
            else:
                role = discord.utils.get(ctx.guild.roles, name='ancap')
                await ctx.author.add_roles(role)
                await ctx.send('Usuário registrado com sucesso!')
        else:
            await ctx.send('Você já está registrado')

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
                await ctx.send(f'Canal {name} criado')
            else:
                await ctx.send(result)
        elif msg.content == 'n':
            await ctx.send('Operação cancelada') 

def setup(client):
    client.add_cog(Economy(client))