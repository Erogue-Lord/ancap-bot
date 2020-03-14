import discord
from discord.ext import commands
import random
from decimal import Decimal
import db

class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = db.conn
        self.cursor = db.cursor

    @commands.command()
    async def moeda(self, ctx, bet: Decimal, side='cara'):
        if side == 'cara':
            number = 1
        elif side == 'coroa':
            number = 2
        else:
            await ctx.send('use "cara" ou "coroa"')
            return 0
        result = random.randint(0, 2)
        if result == number:
            result = db.transaction(ctx.message.author.id, -(bet))
            if result == 0:
                await ctx.send(f'Você ganhou AC${bet:.2f}!')
            else:
                await ctx.send(result)
        else:
            result = db.transaction(ctx.message.author.id, bet)
            if result == 0:
                await ctx.send(f'Você perdeu AC${bet:.2f}')
            else:
                await ctx.send(result)

    @commands.command()
    async def dado(self, ctx, number: int, bet: Decimal):
        result = random.randint(0, 6)
        if result == number:
            result = db.transaction(ctx.message.author.id, -(bet*5))
            if result == 0:
                await ctx.send(f'Você ganhou AC${bet*5:.2f}!')
            else:
                await ctx.send(result)
        else:
            result = db.transaction(ctx.message.author.id, bet)
            if result == 0:
                await ctx.send(f'Você perdeu AC${bet:.2f}')
            else:
                await ctx.send(result)

def setup(client):
    client.add_cog(Gambling(client))