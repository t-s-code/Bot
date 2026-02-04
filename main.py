# main.py
"""
Application entry point.

Responsibilities:
- Initialize Discord client
- Load configuration
- Initialize services
- Route Discord events to the message processor
"""

import discord

from core.dry_run import DryRun
from core.message_processor import MessageProcessor

from channels.config_channel import ConfigChannel
from channels.database_channel import DatabaseChannel
from channels.log_channel import LogChannel

from jobs.member_activity_job import MemberActivityJob
from jobs.channel_pruning_job import ChannelPruningJob


class Bot(discord.Client):
    def __init__(self, is_dry_run, config_channel_id):
        intents = self._build_intents()
        super().__init__(intents=intents)

        self._is_dry_run = is_dry_run
        self._config_channel_id = config_channel_id
        
        self.dry_run = None

        self.config_channel = None
        self.database_channel = None
        self.log_channel = None

        self.member_activity_job = None
        self.channel_pruning_job = None

        self.message_processor = None

    def _build_intents(self) -> discord.Intents:
        """
        Define all Discord intents required by the bot.
        """
        intents = discord.Intents.default()
        intents.message_content = False
        intents.members = False
        return intents

    async def setup_hook(self):
        """
        Initialize services and jobs after Discord connection begins.
        """
        
        self.dry_run = DryRun(
            is_dry_run=self._is_dry_run
        )
        
        self.config_channel = ConfigChannel(
            discord_client=self,
            config_channel_id=self._config_channel_id,
        )

        # TODO: everything below this line will need to get reloaded every time the config is updated
        config = self.config_channel.get_config()
      
        self.database_channel = DatabaseChannel(
            discord_client=self,
            config=config,
        )

        self.log_channel = LogChannel(
            discord_client=self,
            config=config,
        )

        self.member_activity_job = MemberActivityJob(
            discord_client=self,
            dry_run=self.dry_run,
            config=config,
            log_channel=self.log_channel,
            database_channel=self.database_channel,
        )

        self.channel_pruning_job = ChannelPruningJob(
            discord_client=self,
            dry_run=self.dry_run,
            config=config,
            log_channel=self.log_channel,
            database_channel=self.database_channel,
        )

        self.message_processor = MessageProcessor(
            member_activity_job=self.member_activity_job,
            database_channel=self.database_channel,
        )

    async def on_ready(self):
        """
        Called when the bot successfully connects.
        """
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        """
        Delegate message handling to the message processor.
        """
        await self.message_processor.process(message)

    async def run_periodic_jobs(self):
        """
        Background periodic jobs.

        Intended to run:
        - Inactivity sweeps
        - Channel pruning
        """
        pass


def main():
    """
    Application bootstrap.
    """
    # TODO read both of these from command line args
    is_dry_run = None
    config_channel_id = None
    
    bot = Bot(is_dry_run, config_channel_id)

    # Token loading intentionally omitted (config/env later)
    # bot.run("TOKEN")
    pass


if __name__ == "__main__":
    main()
