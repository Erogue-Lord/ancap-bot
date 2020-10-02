import logging
import os
from itertools import cycle

import discord
from discord.ext import commands, tasks

from . import settings

logger = logging.getLogger(__name__)


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
        logger.info(_("We have logged in as {}").format(self.user))
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))

    async def on_command_error(self, ctx, error):
        logger.error(_("Exception occurred\n{}").format(str(error)))

    def load(self):
        for filename in os.listdir(os.path.abspath(os.path.join(__file__, "../cogs"))):
            if filename.endswith(".py") and filename != "__init__.py":
                self.load_extension(f"ancap_bot.cogs.{str(filename)[:-3]}")
