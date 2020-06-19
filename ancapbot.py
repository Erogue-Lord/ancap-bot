import gettext
from inspect import currentframe
import json
from itertools import cycle
import os

import discord
from discord.ext import (commands, tasks)

def load_env():
    config = json.load(open('data/config.json'))
    for sub in config.keys():
        for key, value in config[sub].items():
            os.environ[key] = str(value)

load_env()

t = gettext.translation('base', "./locale", languages=[os.environ['locale']])

def _(s):
    frame = currentframe().f_back
    return eval(f"f'{t.gettext(s)}'", frame.f_locals, frame.f_globals)

class AncapBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.environ["prefix"])
        self.status = cycle([
            discord.Game(name=_("Tax evasion simulator")),
            discord.Activity(type=discord.ActivityType.listening, name=_("Tax evasion hints")),
            discord.Activity(type=discord.ActivityType.watching, name=_("Tax evasion tutorial"))
        ])
        self.load()
        self.run(os.environ["token"])

    async def on_ready(self):
        print(_("We have logged in as {self.user}"))
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))
    '''
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            await ctx.send(_("Something wrong is not right..."))
            print(error)
    '''
    def load(self):
        for filename in os.listdir(os.path.abspath('cogs')):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    AncapBot()