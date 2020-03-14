import discord
from discord.ext import commands

class Adm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Impede um usuário de falar no seu canal')
    async def mute(self, ctx, member):
        channel = ctx.channel
        server = ctx.guild
        target = server.get_member(int(member[3:-1]))
        perm = channel.permissions_for(ctx.message.author).manage_permissions
        if perm:
            await channel.set_permissions(target, send_messages=False)
            await ctx.send(f"Usuário {target} foi mutado")
        else: 
            await ctx.send("Você não tem essa permição")

def setup(client):
    client.add_cog(Adm(client))