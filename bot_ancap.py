import os
from itertools import cycle
import json

import discord
from discord.ext import commands, tasks


class BotAncap(commands.Bot):
    def __init__(self):
        self.config = json.load(open('data/config.json'))["bot"]
        super().__init__(command_prefix=self.config["prefix"])
        self.status = cycle([
            discord.Game(name="sonegador de imposto simulator"),
            discord.Activity(type=discord.ActivityType.listening, name="dicas para sonegar imposto"),
            discord.Activity(type=discord.ActivityType.watching, name="tutorial de como sonegar imposto")
        ])
        self.load()
        self.run(self.config["token"])

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))

    '''
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            await ctx.send('Algo de errado não está certo...')
    '''
    def load(self):
        for filename in os.listdir(os.path.abspath('cogs')):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    BotAncap()