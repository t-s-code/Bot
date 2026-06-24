class OurBot:
    def __init__(self, is_dry_run):
        self._is_dry_run = is_dry_run

        self._discord_client = discord.Client(
            intents=self._build_intents()
        )

        # TODO: when to use?
        self._processing_lock = asyncio.Lock()

        # Jobs
        self._channel_scanning_job = ChannelScanningJob(
            discord_client=self._discord_client,
        )

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

        await self._setup_services()

        asyncio.create_task(self.run_periodic_jobs())

    async def _on_message(self, message):
        await self.message_processor.process_message(message)

    # -------------------------
    # Periodic Jobs
    # -------------------------

    async def run_periodic_jobs(self):
        while True:
            await asyncio.sleep(5 * 60) # five minutes

            async with self._processing_lock:
                await self._channel_scanning_job.scan_for_missed_messages()

    # -------------------------
    # Run
    # -------------------------

    def run(self, token):
        self._discord_client.run(token)
      
