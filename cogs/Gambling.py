import random
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
import texttable
import discord
from discord.ext import commands

import db

class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = db.conn
        self.cursor = db.cursor
    
    def dice(self, sides, bet, number, user):
        result = random.randint(0, sides)
        if result == number:
            result = db.transaction(user, -(bet*(sides-1)))
            if result == 0:
                return f'Você ganhou AC${bet*(sides-1):.2f}!'
            else:
                return result
        else:
            result = db.transaction(user, bet)
            if result == 0:
                return f'Você perdeu AC${bet:.2f}'
            else:
                return result

    @commands.command(help='Joga uma moeda, 2x a aposta caso ganhe')
    async def moeda(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = self.dice(2, bet, 2, user)
        await ctx.send(result)

    @commands.command(help='Rola um dado, 6x a aposta caso ganhe')
    async def dado(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = self.dice(6, bet, 6, user)
        await ctx.send(result)
    
    @commands.command(help='Rola um dado de 20 lados, 20x a aposta caso ganhe')
    async def d20(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = self.dice(20, bet, 20, user)
        await ctx.send(result)
    @commands.command(help='Resultados do jogo do bicho')
    async def bicho(self, ctx):
        page = requests.get('https://www.ojogodobicho.com/deu_no_poste.htm')

        soup = BeautifulSoup(page.text, 'html.parser')

        results = soup.find('table', attrs={'class':'twelve'})
        results_itens = results.find_all('td')
        title = results.find('caption').contents[0]
        contents = [x.contents[0] for x in results_itens]
        chunks = [contents[x:x+6] for x in range(0, len(contents), 6)]
        final = texttable.Texttable()
        final.add_rows([['','PTM','PT', 'PTV', 'FED', 'COR']], header=True)
        for row in chunks:
            final.add_row(row)
        await ctx.send('Resultados do jogo do bicho RJ:\n'+title+'\n```\n'+final.draw()+'\n```')

def setup(client):
    client.add_cog(Gambling(client))