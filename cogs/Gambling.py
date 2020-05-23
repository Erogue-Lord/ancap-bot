import random
from decimal import Decimal
import os
import json

import requests
from bs4 import BeautifulSoup
import texttable
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
                return f'Você ganhou AC${bet*(sides-1):.2f}!'
        else:
            try:
                result = transaction(self.credentials, user, bet)
            except ValueError as error:
                return error
            else:
                return f'Você perdeu AC${bet:.2f}'

    @commands.command(help='Joga uma moeda, 2x a aposta caso ganhe')
    async def coin(self, ctx, bet):
        user = ctx.message.author.id
        result = self.dice_calc(2, bet, 2, user)
        await ctx.send(result)

    @commands.command(help='Rola um dado, 6x a aposta caso ganhe')
    async def dice(self, ctx, bet):
        user = ctx.message.author.id
        result = self.dice_calc(6, bet, 6, user)
        await ctx.send(result)
    
    @commands.command(help='Rola um dado de 20 lados, 20x a aposta caso ganhe')
    async def d20(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = self.dice_calc(20, bet, 20, user)
        await ctx.send(result)

def setup(client):
    client.add_cog(Gambling(client))