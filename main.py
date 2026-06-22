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

from channels.database_channel import DatabaseChannel
from channels.log_channel import LogChannel

from jobs.member_activity_job import MemberActivityJob
from jobs.channel_pruning_job import ChannelPruningJob
from jobs.channel_scanning_job import ChannelScanningJob


class Bot:
    def __init__(self, is_dry_run):
        self._is_dry_run = is_dry_run

        self.discord_client = discord.Client(
            intents=self._build_intents()
        )

        self._processing_lock = asyncio.Lock()

        # Core utilities
        self.dry_run = None

        # Channels
        self.database_channel = None
        self.log_channel = None

        # Jobs
        self.member_activity_job = None
        self.channel_pruning_job = None
        self.channel_scanning_job = None

        # Processing
        self.message_processor = None

        self._register_events()

    # -------------------------
    # Discord Setup
    # -------------------------

    def _build_intents(self):
        intents = discord.Intents.default()
        intents.message_content = False
        intents.members = False
        return intents

    def _register_events(self):
        @self.discord_client.event
        async def on_ready():
            await self._on_ready()

        @self.discord_client.event
        async def on_message(message):
            await self._on_message(message)

    # -------------------------
    # Event Handlers
    # -------------------------

    async def _on_ready(self):
        print(f"Logged in as {self.discord_client.user}")

        await self._setup_services()

        asyncio.create_task(self.run_periodic_jobs())

    async def _on_message(self, message):
        await self.message_processor.process_message(message)

    # -------------------------
    # Service Wiring
    # -------------------------

    async def _setup_services(self):
        self.dry_run = DryRun(is_dry_run=self._is_dry_run)

        # TODO: config channel no longer exists. Just hardcode prod config.
        config = await self.config_channel.get_config()

        # Channels
        self.database_channel = DatabaseChannel(
            discord_client=self.discord_client,
            config=config,
        )

        self.log_channel = LogChannel(
            discord_client=self.discord_client,
            config=config,
        )

        # Jobs
        self.member_activity_job = MemberActivityJob(
            discord_client=self.discord_client,
            dry_run=self.dry_run,
            config=config,
            log_channel=self.log_channel,
            database_channel=self.database_channel,
        )

        self.channel_pruning_job = ChannelPruningJob(
            discord_client=self.discord_client,
            dry_run=self.dry_run,
            config=config,
            log_channel=self.log_channel,
            database_channel=self.database_channel,
        )

        self.channel_scanning_job = ChannelScanningJob(
            discord_client=self.discord_client,
            processing_lock=self._processing_lock,
            database_channel=self.database_channel,
        )

        # Message Processor (depends on jobs)
        self.message_processor = MessageProcessor(
            member_activity_job=self.member_activity_job,
            database_channel=self.database_channel,
            channel_scanning_job=self.channel_scanning_job,
        )

    # -------------------------
    # Periodic Jobs
    # -------------------------

    async def run_periodic_jobs(self):
        while True:
            await asyncio.sleep(5 * 60) # five minutes

            async with self._processing_lock:
                await self.channel_scanning_job.run_scanning_sweep()
                await self.member_activity_job.run_inactivity_sweep()
                await self.channel_pruning_job.run_pruning_sweep()

    # -------------------------
    # Run
    # -------------------------

    def run(self, token):
        self.discord_client.run(token)


def main():
    is_dry_run = None
    token = None

    bot = Bot(is_dry_run)
    # bot.run(token)


if __name__ == "__main__":
    main()
