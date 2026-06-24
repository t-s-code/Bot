# our_bot.py

import asyncio
import discord

from jobs.channel_scanning_job import ChannelScanningJob

class OurBot:
    def __init__(self, is_dry_run, config):
        self._is_dry_run = is_dry_run
        self._config = config

        self._config.validate()

        self._discord_client = discord.Client(
            intents=self._build_intents()
        )

        self._channel_scanning_job = ChannelScanningJob(
            discord_client=self._discord_client
        )

        self._register_events()

    # -------------------------
    # Discord Setup
    # -------------------------

    def _build_intents(self):
        intents = discord.Intents.default()
        intents.message_content = False
        return intents

    def _register_events(self):
        @self._discord_client.event
        async def on_ready():
            await self._on_ready()

        @self._discord_client.event
        async def on_message(message):
            await self._on_message(message)

    # -------------------------
    # Event Handlers
    # -------------------------
  
    async def _on_ready(self):
        print(f"Logged in as {self._discord_client.user}")

        asyncio.create_task(self.run_periodic_jobs())

    async def _on_message(self, message):
        pass

    # -------------------------
    # Periodic Jobs
    # -------------------------

    async def run_periodic_jobs(self):
        while True:
            await asyncio.sleep(5 * 60) # five minutes
            await self._channel_scanning_job.scan_channels()

    # -------------------------
    # Run
    # -------------------------

    def run(self, token):
        self._discord_client.run(token)
      
