import random
from decimal import Decimal

from discord.ext import commands

from .. import db, exceptions


class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def dice_calc(self, sides: int, bet: Decimal, number: int, user: int) -> str:
        result = random.randint(0, sides)
        if result == number:
            try:
                result = await db.transaction(user, -(bet * (sides - 1)))
            except exceptions.AncapBotError as error:
                return str(error)
            else:
                return _("You won AC${:.2f}!").format(bet * (sides - 1))
        else:
            try:
                result = await db.transaction(user, bet)
            except exceptions.AncapBotError as error:
                return str(error)
            else:
                return _("You lost AC${:.2f}").format(bet)

    @commands.command(help=_('Flip a coin, 2x the bet if you win'))
    async def coin(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = await self.dice_calc(2, abs(bet), 2, user)
        await ctx.send(result)

    @commands.command(help=_('Roll a dice, 6x the bet if you win'))
    async def dice(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = await self.dice_calc(6, abs(bet), 6, user)
        await ctx.send(result)

    @commands.command(help=_("Roll a 20 sides dice, 20x the bet if you win"))
    async def d20(self, ctx, bet: Decimal):
        user = ctx.message.author.id
        result = await self.dice_calc(20, abs(bet), 20, user)
        await ctx.send(result)


def setup(client):
    client.add_cog(Gambling(client))
