import os
from itertools import cycle
import configparser

import discord
from discord.ext import commands, tasks

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
def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

def main():
    config = configparser.ConfigParser()
    config.read(os.path.join(__file__, '../data/config.ini'))
    token = config['bot']['token']
    load()
    client.run(token)

if __name__ == "__main__":
    main()