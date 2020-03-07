import discord 
from discord.ext import commands
import sys
import os

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True, help='Uso do dono')
    @commands.is_owner()
    async def off(self, ctx):
        await ctx.send('Desligando...')
        sys.exit()

    @commands.command(hidden=True, help='Uso do dono', name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        await ctx.send(eval(code))

    @commands.command(hidden=True, help='Uso do dono')
    @commands.is_owner()
    async def bash(self, ctx, *, code):
        output = os.popen(code).read()
        try:
            await ctx.send(output)
        except:
            pass

def setup(client):
    client.add_cog(Owner(client))