from gettext import gettext as _
import os
from itertools import cycle
import json

import discord
from discord.ext import (commands, tasks)


class AncapBot(commands.Bot):
    def __init__(self):
        self.config = json.load(open('data/config.json'))["bot"]
        super().__init__(command_prefix=self.config["prefix"])
        self.status = cycle([
            discord.Game(name=_("Tax evasion simulator")),
            discord.Activity(type=discord.ActivityType.listening, name=_("Tax evasion hints")),
            discord.Activity(type=discord.ActivityType.watching, name=_("Tax evasion tutorial"))
        ])
        self.load()
        self.run(self.config["token"])

    async def on_ready(self):
        print(_(f"We have logged in as {self.user}"))
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            await ctx.send(_("Something wrong is not right..."))
            print(error)

    def load(self):
        for filename in os.listdir(os.path.abspath('cogs')):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    AncapBot()