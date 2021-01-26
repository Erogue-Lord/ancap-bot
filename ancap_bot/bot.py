import logging
from itertools import cycle

import discord
from discord.ext import commands, tasks
from tortoise import Tortoise

from . import settings, db


class AncapBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=settings.PREFIX)
        self.logger = logging.getLogger(__name__)
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
        try:
            self.loop.run_until_complete(self.start(settings.TOKEN))
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(Tortoise.close_connections())
            self.loop.close()
            self.logger.info(_("Bot logged out"))

    async def on_ready(self):
        await db.init()
        self.load()
        self.logger.info(_("We have logged in as {}").format(self.user))
        self.status_change.start()

    @tasks.loop(seconds=30)
    async def status_change(self):
        await self.change_presence(activity=next(self.status))

    async def on_command_error(self, ctx, error):
        self.logger.error(_("Exception occurred\n{}").format(str(error)))

    def load(self):
        for cog in ("adm", "basics", "economy", "gambling"):
            self.load_extension(f"ancap_bot.cogs.{cog}")
