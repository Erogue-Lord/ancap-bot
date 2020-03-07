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
        self.cursor.execute(f'''
        select balance from users where user_id = {user_id}
        ''')
        balance = Decimal(self.cursor.fetchall()[0][0])
        if balance >= amount:
            try:
                self.cursor.execute(f'''
                UPDATE users
                SET balance = balance - {amount}
                WHERE user_id = {user_id};
                ''')
                self.cursor.execute(f'''
                UPDATE users
                SET balance = balance + {amount}
                WHERE user_id = {target_id}; 
                ''')
                self.conn.commit()
            except:
                await ctx.send('Falha na transação')
            else:
                server = ctx.guild
                name = server.get_member(target_id)
                await ctx.send(f'AC${amount:.2f} foram tranferidos para {name}')
        else:
            await ctx.send('Você não tem esse dinheiro')    

def setup(client):
    client.add_cog(Economy(client))