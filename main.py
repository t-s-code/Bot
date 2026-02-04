# main.py
"""
Application entry point.

Responsibilities:
- Initialize Discord client
- Wire services and jobs together
- Schedule high level bot workflows
"""

import asyncio
import discord

from core.dry_run import DryRun
from core.message_processor import MessageProcessor

from channels.config_channel import ConfigChannel
from channels.database_channel import DatabaseChannel
from channels.log_channel import LogChannel

from jobs.member_activity_job import MemberActivityJob
from jobs.channel_pruning_job import ChannelPruningJob
from jobs.channel_scanning_job import ChannelScanningJob


class Bot(discord.Client):
    def __init__(self, is_dry_run, config_channel_id):
        intents = self._build_intents()
        super().__init__(intents=intents)

        self._is_dry_run = is_dry_run
        self._config_channel_id = config_channel_id

        self._processing_lock = asyncio.Lock()

        self.dry_run = None

        self.config_channel = None
        self.database_channel = None
        self.log_channel = None

        self.member_activity_job = None
        self.channel_pruning_job = None
        self.channel_scanning_job = None
        
        self.message_processor = None

    def _build_intents(self) -> discord.Intents:
        intents = discord.Intents.default()
        intents.message_content = False
        intents.members = False
        return intents

    async def setup_hook(self):
        self.dry_run = DryRun(is_dry_run=self._is_dry_run)

        self.config_channel = ConfigChannel(
            discord_client=self,
            config_channel_id=self._config_channel_id,
        )

        config = await self.config_channel.get_config()

        self._build_config_dependent_services(config)

        asyncio.create_task(self.run_periodic_jobs())

    def _build_config_dependent_services(self, config):
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
        
        self.channel_scanning_job = ChannelScanningJob(
            discord_client=self,
            processing_lock=self._processing_lock,
            message_processor=self.message_processor,
            database_channel=self.database_channel,
        )
    
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.channel_scan_job.schedule_scan(
            channel_id=message.channel.id
        )

    async def run_periodic_jobs(self):
        """
        Background periodic jobs.
        """
        while True:
            await asyncio.sleep(300)

            async with self._processing_lock:
                await self.channel_scanning_job.run_scanning_sweep()
                await self.member_activity_job.run_inactivity_sweep()
                await self.channel_pruning_job.run_pruning_sweep()
                
    async def request_hot_reload(self):
        """
        Reload config safely when bot is idle.
        """
        async with self._processing_lock:
            config = await self.config_channel.get_config()
            self._build_config_dependent_services(config)


def main():
    is_dry_run = None
    config_channel_id = None

    bot = Bot(is_dry_run, config_channel_id)

    # bot.run("TOKEN")
    pass


if __name__ == "__main__":
    main()
