from gettext import gettext as _
import discord
from discord.ext import commands

class Adm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help=_("Hire private police (moderators) for your channel"))
    async def mod(self, ctx, user):
        channel = ctx.channel
        server = ctx.guild
        target = server.get_member(ctx.message.mentions[0].id)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
            return None
        await channel.set_permissions(target, manage_messages=True, send_messages=True)
        await ctx.send(_(f"User {target} has been promoted to moderator!"))

    @commands.command(help=_("Remove moderator"))
    async def demote(self, ctx, user):
        channel = ctx.channel
        server = ctx.guild
        target = server.get_member(ctx.message.mentions[0].id)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
            return None
        await channel.set_permissions(target, manage_messages=False)
        await ctx.send(_(f"User {target} has been demoted"))

    @commands.command(help=_("Mute an user in your channel"))
    async def mute(self, ctx, user):
        server = ctx.guild
        if user == '*':
            target = server.default_role
            message = _("All users have been muted")
        else:
            target = server.get_member(ctx.message.mentions[0].id)
            message = _(f"User {target} has been muted")
        channel = ctx.channel
        perm = channel.permissions_for(ctx.message.author).manage_messages
        if perm:
            await channel.set_permissions(target, send_messages=False)
            await ctx.send(message)
        else:
            await ctx.send(_("You dont have that permission"))
            
    @commands.command(help=_("Unmute an user"))
    async def unmute(self, ctx, user):
        server = ctx.guild
        if user == '*':
            target = server.default_role
            message = _("All users have been unmuted")
        else:
            target = server.get_member(ctx.message.mentions[0].id)
            message = _(f"User {target} has been muted")
        channel = ctx.channel
        perm = channel.permissions_for(ctx.message.author).manage_messages
        if perm:
            await channel.set_permissions(target, send_messages=True)
            await ctx.send(message)
        else:
            await ctx.send(_("You dont have that permission"))

    @commands.command(help=_("Delete the channel"))
    async def delete(self, ctx):
        def check(message):
            return message.author == ctx.message.author and (message.content == _('y') or message.content == _('n'))
        server = ctx.guild
        channel = ctx.channel
        deleted_channel = discord.utils.get(server.channels, name=channel.name)
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
            return None
        else:
            await ctx.send(_("You realy want to delete this channel?[y/n]"))
            msg = await self.client.wait_for('message', check=check, timeout=30)
            if msg.content == _('y'):
                try:
                    await role.delete()
                except:
                    pass
                await deleted_channel.delete()
            elif msg.content == _('n'):
                await ctx.send(_("Operation canceled"))

    @commands.command(help=_("Toggles NSFW in your channel"))
    async def nsfw(self, ctx):
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
        else:
            if channel.nsfw:
                await channel.edit(nsfw=False)
                await ctx.send(_(f"{channel.name} Isn't NSFW anymore"))
            else:
                await channel.edit(nsfw=True)
                await ctx.send(_(f"{channel.name} Isn NSFW now"))

    @commands.command(help=_("Activate slowmode with the especified seconds"))
    async def slowmode(self, ctx, time: int):
        if time > 21600:
            await ctx.send(_("The limit is 21600 seconds"))
            return None
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
        else:
            await channel.edit(slowmode_delay=time)
            if time == 0:
                await ctx.send(_("Slowmode deactivated"))
            else:
                await ctx.send(_(f"{time} seconds slowmode activated"))

    @commands.command(help=_("Change your channel topic"))
    async def topic(self, ctx, *, topic: str):
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send(_("You dont have that permission"))
        else:
            await channel.edit(topic=topic)
            await ctx.send(_(f'Topic changed to "{topic}"'))

def setup(client):
    client.add_cog(Adm(client))