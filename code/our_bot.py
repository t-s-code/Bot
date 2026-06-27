# our_bot.py

import asyncio
import discord

from core.database import Database
from jobs import ChannelScanningJob

class OurBot:
    def __init__(self, is_dry_run, config):
        self._is_dry_run = is_dry_run
        self._config = config

        self._config.validate()

        self._discord_client = discord.Client(
            intents=self._build_intents()
        )

        self._database = Database(self._discord_client)

        self._channel_scanning_job = ChannelScanningJob(
            discord_client=self._discord_client,
            database=self._database,
            config=self._config
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

        await self._database.load()
        asyncio.create_task(self._channel_scanning_job.run())

    async def _on_message(self, message):
        pass

    # -------------------------
    # Run
    # -------------------------

    def run(self, token):
        self._discord_client.run(token)
