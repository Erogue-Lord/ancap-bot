"""MIT License Copyright (c) 2020 Erogue Lord

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
from itertools import cycle

import discord
from discord.ext import commands, tasks

from . import settings


class AncapBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=settings.PREFIX)
        self.status = cycle(
            [
                discord.Game(name=_("Tax evasion simulator")),
                discord.Activity(
                    type=discord.ActivityType.listening, name=_("Tax evasion hints")
                ),
                discord.Activity(
                    type=discord.ActivityType.watching, name=_("Tax evasion tutorial")
                ),
            ]
        )
        self.load()
        self.run(settings.TOKEN)

    async def on_ready(self):
        print(_("We have logged in as {}").format(self.user))
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            await ctx.send(_("Something wrong is not right..."))
            raise error

    def load(self):
        for filename in os.listdir(os.path.join(__file__, "../cogs")):
            if filename.endswith(".py") and filename != "__init__.py":
                self.load_extension(f"ancap_bot.cogs.{filename[:-3]}")
