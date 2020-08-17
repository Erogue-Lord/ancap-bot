import re
from datetime import datetime, timedelta
from decimal import Decimal

import discord
from discord.ext import commands

from .. import _, db, settings


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    def registrate(self, id: int, session):
        user = db.User(user_id=id)
        session.add(user)

    def pay(self, now: datetime, _id: int, session) -> str:
        user = db.User.get_by_id(_id, session)
        user.balance += settings.WAGE
        user.work = now
        return _("You earned AC${}").format(settings.WAGE)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with db.session_scope() as session:
            self.registrate(member.id, session)
        role = discord.utils.get(member.guild.roles, name="ancap")
        await member.add_roles(role)

    @commands.command(help=_("Create your acount"))
    async def init(self, ctx):
        _id = ctx.author.id
        with db.session_scope() as session:
            user = db.User.get_by_id(_id, session)
            if user is None:
                self.registrate(_id, session)
                role = discord.utils.get(ctx.guild.roles, name="ancap")
                await ctx.author.add_roles(role)
                await ctx.send(_("User successfully registered!"))
            else:
                await ctx.send(_("You're already registered"))

    @commands.command(help=_("Make money (can be used after a time interval)"))
    async def work(self, ctx):
        _id = ctx.author.id
        with db.session_scope() as session:
            user = db.User.get_by_id(_id, session)
            if user is not None:
                date = user.work
            else:
                await ctx.send(_("Use $init to create an acount"))
                return
            now = datetime.now()
            if date is None:
                await ctx.send(self.pay(now, _id, session))
            else:
                if date + timedelta(seconds=settings.COOLDOWN) <= now:
                    await ctx.send(self.pay(now, _id, session))
                else:
                    interval = (date + timedelta(seconds=settings.COOLDOWN)) - now
                    cooldown = interval - timedelta(microseconds=interval.microseconds)
                    await ctx.send(
                        _("You have to wait {} to work again").format(cooldown)
                    )

    @commands.command(help=_("Show your balance"))
    async def balance(self, ctx):
        _id = ctx.author.id
        with db.session_scope() as session:
            user = db.User.get_by_id(_id, session)
            if user is not None:
                balance = user.balance
                await ctx.send(_("{} have AC${:.2f}").format(ctx.author, balance))
            else:
                await ctx.send(
                    _("You are not registered, use $init to create an bank acount")
                )

    @commands.command(help=_("Transfers money to someone"))
    async def trans(self, ctx, amount, user):
        amount = abs(Decimal(amount))
        target_id = ctx.message.mentions[0].id
        user_id = ctx.author.id
        server = ctx.guild
        try:
            result = db.transaction(user_id, amount, target_id)
        except ValueError as error:
            result = error
        else:
            result = _("AC${:.2f} have been transferred to {}").format(
                amount, server.get_member(target_id)
            )
        await ctx.send(result)

    @commands.command(help=_("Buy a channel for you"))
    async def channel(self, ctx, *, name):
        def check(message):
            return message.author == ctx.message.author and (
                message.content == _("y") or message.content == _("n")
            )

        server = ctx.guild
        category = discord.utils.get(server.categories, name=settings.CHANNEL_CATEGORY)
        name = re.findall("[a-z,0-9,_, ]*", name.lower())
        name = "".join(name)
        if len(name) < 1:
            await ctx.send(_("Invalid name"))
            return
        name = "".join(name)
        new_channel = discord.utils.get(server.channels, name=name)
        if new_channel:
            await ctx.send(
                _(
                    "A channel with that name already exist! \
                    Try to create with another one"
                )
            )
            return
        await ctx.send(_("You want to buy a channel? This will cost you AC$100[y/n]"))
        msg = await self.client.wait_for("message", check=check, timeout=30)
        if msg.content == _("y"):
            user = ctx.message.author
            _id = user.id
            try:
                result = db.transaction(_id, settings.CHANNEL_PRICE)
            except ValueError as error:
                result = error
            else:
                channel = await server.create_text_channel(name, category=category)
                role = await server.create_role(name=channel.name)
                await channel.set_permissions(
                    role, manage_messages=True, send_messages=True
                )
                await user.add_roles(role)
                result = _("{} Channel was created").format(channel.name)
            await ctx.send(result)
        elif msg.content == _("n"):
            await ctx.send(_("Operation canceled"))


def setup(client):
    client.add_cog(Economy(client))
