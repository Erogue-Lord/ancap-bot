import discord
from discord.ext import commands
from decimal import getcontext, Decimal
import configparser
from datetime import datetime
from datetime import timedelta
import db

getcontext().prec = 3

class Economy(commands.Cog):
    def __init__(self, client):
        self.config = configparser.ConfigParser()
        self.client = client
        self.conn = db.conn
        self.cursor = db.cursor

    def registrate(self, id):
        self.cursor.execute(f'''
        INSERT into users (user_id, balance)
        VALUES ({id}, 0.00);
        ''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.registrate(member.id)
        role = discord.utils.get(member.guild.roles, name='ancap')
        await member.add_roles(role)

    @commands.command(help='Cria sua conta')
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

    @commands.command(help='Ganha dinheiro (pode ser usado de 1 em 1 minuto)')
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
                balance = balance + 25
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
                    balance = balance + 25
                WHERE
                    user_id = {_id};
                ''')
                self.conn.commit()
                await ctx.send("Você ganhou AC$25.00")
            else:
                intervalo = (date + timedelta(minutes=1)) - now
                await ctx.send(f"Você tem que esperar {intervalo - timedelta(microseconds=intervalo.microseconds)} para trabalhar novamente")


    @commands.command(help='Mostra seu saldo')
    async def saldo(self, ctx):
        user_id = ctx.author.id
        self.cursor.execute(f'''
        select balance::money::numeric::float8 from users where user_id = {user_id}
        ''')
        try:
            balance = Decimal(self.cursor.fetchall()[0][0])
        except:
            await ctx.send('Você não está registrado, use $init para criar sua conta bancária')
        else:
            await ctx.send(f'{ctx.author} tem AC${balance:.2f}')

    @commands.command(help='da dinheiro ao seu amiguinho')
    async def trans(self, ctx, amount: Decimal, user):
        target_id = int(user[3:-1])
        user_id = ctx.author.id
        server = ctx.guild
        result = db.transaction(user_id, amount, target_id)
        if result == 0:
            result = f'AC${amount:.2f} foram tranferidos para {server.get_member(target_id)}'
        await ctx.send(result)

    @commands.command(help='Compra um canal só seu')
    async def canal(self, ctx, *, name):
        def check(message):
            return message.author == ctx.message.author and (message.content == "s" or message.content == "n")
        name = name.replace(' ', '-').lower()
        guild = ctx.guild
        new_channel = discord.utils.get(guild.channels, name=name)
        if new_channel != None:
            await ctx.send('Um canal com esse nome ja existe! Tente criar com outro nome')
            return 0
        await ctx.send('Você quer criar um canal? isso ira te custar AC$100[s/n]')
        msg = await self.client.wait_for('message', check=check, timeout=30)
        if msg.content == 's':
            user = ctx.message.author
            _id = user.id
            result = db.transaction(_id, 100.00)
            if result == 0:
                category = discord.utils.get(guild.categories, name='Canais de Texto')
                await guild.create_text_channel(name, category=category)
                channel = discord.utils.get(guild.channels, name=name)
                await guild.create_role(name=name)
                role = discord.utils.get(ctx.guild.roles, name=name)
                await user.add_roles(role)
                await channel.set_permissions(role, manage_messages=True, send_messages=True)
                await ctx.send(f'Canal {name} criado')
            else:
                await ctx.send(result)
        elif msg.content == 'n':
            await ctx.send('Operação cancelada')

def setup(client):
    client.add_cog(Economy(client))