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
    
    @commands.command(help='deleta um canal')
    async def deletar(self, ctx):
        def check(message):
            return message.author == ctx.message.author and (message.content == "s" or message.content == "n")
        server = ctx.guild
        channel = ctx.channel
        deleted_channel = discord.utils.get(server.channels, name=channel.name)
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
            return 0
        else:
            await ctx.send("Você quer deletar esse canal?[s/n]")
            msg = await self.client.wait_for('message', check=check, timeout=30)
            if msg.content == 's':
                try:
                    await role.delete()
                except:
                    pass
                await deleted_channel.delete()
            elif msg.content == 'n':
                await ctx.send("Operação cancelada")

    @commands.command(help='Deixa seu canal NSFW')
    async def nsfw(self, ctx):
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
        else:
            if channel.nsfw:
                await channel.edit(nsfw=False)
                await ctx.send(f"{channel.name} deixou de ser NSFW")
            else:
                await channel.edit(nsfw=True)
                await ctx.send(f"{channel.name} agora é NSFW")

    @commands.command(help='bota slowmode no canal por n segundos')
    async def slowmode(self, ctx, time: int):
        if time > 21600:
            await ctx.send("O limite é 21600 segundos")
            return 0
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
        else:
            await channel.edit(slowmode_delay=time)
            if time == 0:
                await ctx.send("Slowmode desativado")
            else:
                await ctx.send(f"Slowmode de {time} segundos ativado")

    @commands.command(help='Muda o tópico do seu canal')
    async def topico(self, ctx, *, topic: str):
        server = ctx.guild
        channel = ctx.channel
        role = discord.utils.get(server.roles, name=channel.name)
        roles = [role.name for role in ctx.message.author.roles]
        if not channel.name in roles:
            await ctx.send("Você não tem essa permição")
        else:
            await channel.edit(topic=topic)
            await ctx.send(f'Tópico alterado para "{topic}"')

def setup(client):
    client.add_cog(Adm(client))