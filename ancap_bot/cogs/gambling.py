import random
from decimal import Decimal

from discord.ext import commands

from .. import _, db


class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client

    def dice_calc(self, sides, bet, number, user) -> str:
        result = random.randint(0, sides)
        bet = Decimal(bet)
        if result == number:
            try:
                result = db.transaction(user, -(bet * (sides - 1)))
            except ValueError as error:
                return error
            else:
                return _("You won AC${:.2f}!").format(bet * (sides - 1))
        else:
            try:
                result = db.transaction(user, bet)
            except ValueError as error:
                return error
            else:
                return _("You lost AC${:.2f}").format(bet)

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
    async def d20(self, ctx, bet):
        user = ctx.message.author.id
        result = self.dice_calc(20, bet, 20, user)
        await ctx.send(result)


def setup(client):
    client.add_cog(Gambling(client))
