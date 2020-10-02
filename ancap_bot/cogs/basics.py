import discord
from discord.ext import commands

from .. import __version__, __author__


class Basics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help=_("calculates bot latency"))
    async def ping(self, ctx):
        latency = int(round(self.client.latency * 1000, 0))
        await ctx.send(f"Pong! {latency}ms")

    @commands.command(help=_("Bot info"))
    async def info(self, ctx):
        msg = _(
            "This bot was created to simulate an anarcho-capitalist economy on Discord"
        )
        embed = discord.Embed(
            title=_("An Anarcho-capitalist Bot"),
            description=(msg + "\n[GitHub](https://github.com/Erogue-Lord/ancap-bot)"),
            color=0xFAFF00,
        )

        embed.set_author(name=f"Ancap Bot {__version__}")
        embed.set_footer(text=_("Created by {}").format(__author__))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Basics(client))
