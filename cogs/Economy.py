from decimal import Decimal
from datetime import (datetime, timedelta)
import re
import json
import os

import discord
from discord.ext import commands

from db import (DataBase, transaction)

class Economy(commands.Cog):
    def __init__(self, client):
        self.config = json.load(open('data/config.json'))
        self.client = client

    def registrate(self, id: int):
        with DataBase(self.config["db"]) as db:
            db.cursor.execute(f'''
            INSERT into users (user_id, balance)
            VALUES ({id}, 0.00);
            ''')
    
    def pay(self, now: datetime, _id: int) -> str:
        with DataBase(self.config["db"]) as db:
            db.cursor.execute(f'''
            UPDATE users
            SET 
                work = '{now}',
                balance = balance + {self.config["bot"]["wage"]}
            WHERE
                user_id = {_id};
            ''')
        return f'Você ganhou AC${self.config["bot"]["wage"]:.2f}'

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.registrate(member.id)
        role = discord.utils.get(member.guild.roles, name='ancap')
        await member.add_roles(role)

    @commands.command(help='Cria sua conta')
    async def init(self, ctx):
        _id = ctx.author.id
        with DataBase(self.config["db"]) as db:
            db.cursor.execute(f'''
            select user_id from users where user_id = {_id};
            ''')
            result = db.cursor.fetchall()
        if len(result) == 0:
            self.registrate(_id)
            role = discord.utils.get(ctx.guild.roles, name='ancap')
            await ctx.author.add_roles(role)
            await ctx.send('Usuário registrado com sucesso!')
        else:
            await ctx.send('Você já está registrado')

    @commands.command(help='Ganha dinheiro (pode ser usado depois de um intervalo de tempo)')
    async def trabalhar(self, ctx):
        _id = ctx.author.id
        with DataBase(self.config["db"]) as db:
            db.cursor.execute(f'''
            select work from users where user_id = {_id};
            ''')
            try:
                date = db.cursor.fetchall()[0][0]
            except:
                await ctx.send("use $init para criar uma conta")
                return 0
        now = datetime.now()
        if date == None:
            await ctx.send(self.pay(now, _id))
        else:
            if date + timedelta(seconds=self.config["bot"]["cooldown"]) <= now:
                await ctx.send(self.pay(now, _id))
            else:
                intervalo = (date + timedelta(seconds=self.cooldown)) - now
                await ctx.send(f"Você tem que esperar {intervalo - timedelta(microseconds=intervalo.microseconds)} para trabalhar novamente")


    @commands.command(help='Mostra seu saldo')
    async def saldo(self, ctx):
        user_id = ctx.author.id
        with DataBase(self.config["db"]) as db:
            db.cursor.execute(f'''
            select balance::money::numeric::float8 from users where user_id = {user_id}
            ''')
            try:
                balance = Decimal(db.cursor.fetchall()[0][0])
            except:
                await ctx.send('Você não está registrado, use $init para criar sua conta bancária')
            else:
                await ctx.send(f'{ctx.author} tem AC${balance:.2f}')

    @commands.command(help='da dinheiro ao seu amiguinho')
    async def trans(self, ctx, amount, user):
        amount = abs(Decimal(amount))
        target_id = ctx.message.mentions[0].id
        user_id = ctx.author.id
        server = ctx.guild
        try:
            result = transaction(self.config["db"], user_id, amount, target_id)
        except ValueError as error:
            result = error
        else:
            result = f'AC${amount:.2f} foram tranferidos para {server.get_member(target_id)}'
        await ctx.send(result)

    @commands.command(help='Compra um canal só seu')
    async def canal(self, ctx, *, name):
        def check(message):
            return message.author == ctx.message.author and (message.content == "s" or message.content == "n")
        server = ctx.guild
        category = discord.utils.get(server.categories, name=self.config["bot"]["text_channel_category"])
        name = re.findall('[a-z,0-9,_, ]*', name.lower())
        name = ''.join(name)
        if len(name) < 1:
            await ctx.send("nome invalido")
            return 0
        name = ''.join(name)
        new_channel = discord.utils.get(server.channels, name=name)
        if new_channel:
            await ctx.send('Um canal com esse nome ja existe! Tente criar com outro nome')
            return 0
        await ctx.send('Você quer criar um canal? isso ira te custar AC$100[s/n]')
        msg = await self.client.wait_for('message', check=check, timeout=30)
        if msg.content == 's':
            user = ctx.message.author
            _id = user.id
            try:
                result = transaction(self.config["db"], _id, Decimal(self.config["bot"]["channel_price"]))
            except ValueError as error:
                result = error
            else:
                channel = await server.create_text_channel(name, category=category)
                role = await server.create_role(name=channel.name)
                await channel.set_permissions(role, manage_messages=True, send_messages=True)
                await user.add_roles(role)
                result = f'Canal {channel.name} criado'
            await ctx.send(result)
        elif msg.content == 'n':
            await ctx.send('Operação cancelada')

def setup(client):
    client.add_cog(Economy(client))