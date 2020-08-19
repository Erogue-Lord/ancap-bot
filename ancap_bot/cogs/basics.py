from textwrap import dedent

import discord
from discord.ext import commands


class Basics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="calculates bot latency")
    async def ping(self, ctx):
        latency = int(round(self.client.latency * 1000, 0))
        await ctx.send(f"Pong! {latency}ms")

    @commands.command(help="Bot info")
    async def info(self, ctx):
        embed = discord.Embed(
            title=_("An Anarcho-capitalist Bot"),
            description=dedent(
                _(
                    """\
                This bot was created to simulate an anarcho-capitalist economy on Discord
                [GitHub](https://github.com/Erogue-Lord/ancap-bot)
                """  # noqa: E501
                )
            ),
            color=0xFAFF00,
        )

        embed.set_author(name="Ancap Bot")
        embed.set_footer(text="Created by @Erogue Lord#2332")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Basics(client))
