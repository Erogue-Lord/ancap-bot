import discord
from discord.ext import commands
import sys

class Basics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        latency = int(round(self.client.latency * 1000, 0))
        await ctx.send(f'Pong! {latency}ms')

    @commands.command(hidden=True, help='Um comando secreto...')
    async def ah(self, ctx):
        await ctx.send('Negão')

    @commands.command()
    async def math(self, ctx, *, calc):
        try:
            result = eval(calc, {"__builtins__":None})
        except:
            result = 'Expreção Inválida'
        await ctx.send(result)

    @commands.command()
    async def canal(self, ctx, *, name):
        def check(message):
            return message.author == ctx.message.author and (message.content == "s" or message.content == "n")
        await ctx.send('vc quer criar sum canal?[s/n]')
        msg = await self.client.wait_for('message', check=check)
        
        guild = ctx.guild
        name = name.replace(' ', '-')
        category = discord.utils.get(guild.categories, name='Canais de Texto')
        await guild.create_text_channel(name, category=category)
        await ctx.send(f'Canal {name} criado')

    @commands.command()
    async def info(self, ctx):
        embed=discord.Embed(title="Um Bot Anarcocapitalista", 
        description="Esse bot foi criado para simular uma economia anarcocapitalista no discord\n[github](https://github.com/Erogue-Lord/bot-ancap)", 
        color=0xfaff00)
        embed.set_author(name="Bot Ancap")
        embed.set_footer(text="criado bor @Erogue Lord#2332")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Basics(client))