import discord
from discord.ext import commands

class Adm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='contrata polícia privada(moderadores) pro seu canal')
    async def mod(self, ctx, user):
        channel = ctx.channel
        server = ctx.guild
        target = server.get_member(ctx.message.mentions[0].id)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
            return 0
        await channel.set_permissions(target, manage_messages=True, send_messages=True)
        await ctx.send(f'Usuário {target} promovido a moderador!')

    @commands.command()
    async def demote(self, ctx, user):
        channel = ctx.channel
        server = ctx.guild
        target = server.get_member(ctx.message.mentions[0].id)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
            return 0
        await channel.set_permissions(target, manage_messages=False)
        await ctx.send(f'Usuário {target} rebaixado')

    @commands.command(help='Impede um usuário de falar no seu canal')
    async def mute(self, ctx, user):
        server = ctx.guild
        if user == '*':
            target = server.default_role
            message = 'Todos os usuários foram mutados'
        else:
            target = server.get_member(ctx.message.mentions[0].id)
            message = f"Usuário {target} foi mutado"
        channel = ctx.channel
        perm = channel.permissions_for(ctx.message.author).manage_messages
        if perm:
            await channel.set_permissions(target, send_messages=False)
            await ctx.send(message)
        else: 
            await ctx.send("Você não tem essa permição")

    @commands.command(help='Impede um usuário de falar no seu canal')
    async def unmute(self, ctx, user):
        server = ctx.guild
        if user == '*':
            target = server.default_role
            message = 'Todos os usuários foram desmutados'
        else:
            target = server.get_member(ctx.message.mentions[0].id)
            message = f"Usuário {target} foi desmutado"
        channel = ctx.channel
        perm = channel.permissions_for(ctx.message.author).manage_messages
        if perm:
            await channel.set_permissions(target, send_messages=True)
            await ctx.send(message)
        else: 
            await ctx.send("Você não tem essa permição")

def setup(client):
    client.add_cog(Adm(client))