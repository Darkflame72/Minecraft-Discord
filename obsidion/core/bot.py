"""Main bot file."""
from datetime import datetime

import discord
from discord.ext.commands import AutoShardedBot

from .global_checks import init_global_checks
from .core_commands import Core
from .events import Events
from .config import get_settings


class Obsidion(AutoShardedBot):
    """Main bot class."""

    def __init__(self, *args, **kwargs):
        """Initialise bot with args passed through."""
        super().__init__(*args, **kwargs)

        self.uptime = None
        self.color = discord.Embed.Empty
        self._last_exception = None

    async def pre_flight(self):
        init_global_checks(self)

        # Load important cogsw
        self.add_cog(Events(self))
        self.add_cog(Core(self))
        if get_settings().DEV:
            from .dev_commands import Dev

            self.add_cog(Dev(self))

        # load cogs

    async def start(self, *args, **kwargs):
        """
        Overridden start which ensures cog load and other pre-connection tasks are handled
        """
        await self.pre_flight()
        return await super().start(*args, **kwargs)

    async def message_eligible_as_command(self, message: discord.Message) -> bool:
        """
        Runs through the things which apply globally about commands
        to determine if a message may be responded to as a command.

        This can't interact with permissions as permissions is hyper-local
        with respect to command objects, create command objects for this
        if that's needed.

        This also does not check for prefix or command conflicts,
        as it is primarily designed for non-prefix based response handling
        via on_message_without_command

        Parameters
        ----------
        message
            The message object to check

        Returns
        -------
        bool
            Whether or not the message is eligible to be treated as a command.
        """

        channel = message.channel
        guild = message.guild

        if message.author.bot:
            return False

        if guild:
            assert isinstance(channel, discord.abc.GuildChannel)  # nosec
            if not channel.permissions_for(guild.me).send_messages:
                return False
        #     if not (await self.ignored_channel_or_guild(message)):
        #         return False

        # if not (await self.allowed_by_whitelist_blacklist(message.author)):
        #     return False

        return True
