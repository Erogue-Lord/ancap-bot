from gettext import gettext as _
import random
from decimal import Decimal
import os
import json

import requests
import discord
from discord.ext import commands

from db import transaction

class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.credentials = json.load(open('data/config.json'))["db"]

    def dice_calc(self, sides, bet, number, user) -> str:
        result = random.randint(0, sides)
        if result == number:
            try:
                result = transaction(self.credentials, user, -(bet*(sides-1)))
            except ValueError as error:
                return error
            else:
                return _(f"You won AC${bet*(sides-1):.2f}!")
        else:
            try:
                result = transaction(self.credentials, user, bet)
            except ValueError as error:
                return error
            else:
                return _(f"You lost AC${bet:.2f}")

    @commands.command(help=_("Flip a coin, 2x the bet if you win"))
    async def coin(self, ctx, bet):
        user = ctx.message.author.id
        result = self.dice_calc(2, bet, 2, user)
        await ctx.send(result)

    @commands.command(help=_("Roll a dice, 6x the bet if you win"))
    async def dice(self, ctx, bet):
        user = ctx.message.author.id
        result = self.dice_calc(6, bet, 6, user)
        await ctx.send(result)

    @commands.command(help=_("Roll a 20 sides dice, 20x the bet if you win"))
    async def d20(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = self.dice_calc(20, bet, 20, user)
        await ctx.send(result)

def setup(client):
    client.add_cog(Gambling(client))