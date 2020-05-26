import gettext.gettext as _
import discord
from discord.ext import commands

class Basics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help=_("calculates bot latency"))
    async def ping(self, ctx):
        latency = int(round(self.client.latency * 1000, 0))
        await ctx.send(f(_("Pong! {latency}ms")))

    @commands.command(help=_("Bot info"))
    async def info(self, ctx):
        embed=discord.Embed(title=_("An Anarcho-capitalist Bot"), 
        description=_("This bot was created to simulate and anarcho-capitalist economy on Discord\n[GitHub](https://github.com/Erogue-Lord/ancap-bot)"), 
        color=0xfaff00)
        embed.set_author(name="Ancap Bot")
        embed.set_footer(text=_("Created by @Erogue Lord#2332"))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Basics(client))