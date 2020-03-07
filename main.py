import discord
from discord.ext import commands, tasks
import os
from itertools import cycle

client = commands.Bot(command_prefix='$')
status = cycle([
    discord.Game(name="sonegador de imposto simulator"),
    discord.Activity(type=discord.ActivityType.listening, name="dicas para sonegar imposto"),
    discord.Activity(type=discord.ActivityType.watching, name="tutorial de como sonegar imposto")
    ])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    status_change.start()

@tasks.loop(seconds=30)
async def status_change():
    await client.change_presence(activity=next(status))

'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandError):
        await ctx.send('Algo de errado não está certo...')
'''

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    try:
        token = open('token.txt').read()
        client.run(token)
    except FileNotFoundError:
        token = input('token: ')
        file = open('token.txt', 'w')
        file.write(token)
        file.close()
        client.run(token)
    except discord.errors.LoginFailure:
        print('Erro de Autenticação')