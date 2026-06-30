# core/database.py

import asyncio
from .in_memory_database import InMemoryDatabase

class Database:
    def __init__(self, discord_client):
        self._discord_client = discord_client
        self._lock = asyncio.Lock()
        self._in_memory_database = None

    async def load(self):
        async with self._lock:
            # TODO: messages_from_db = load all messages from the #bot-database channel
            messages_from_db = []
            self._in_memory_database = InMemoryDatabase(messages_from_db)

    async def get_channel_scanning_cursor(self, channel_id):
        async with self._lock:
            return self._in_memory_database.get_channel_scanning_cursor(channel_id)

    async def get_member_activity(self, user_id):
        async with self._lock:
            return self._in_memory_database.get_member_activity(user_id)

    def queue_update(self, record):
        # TODO
        pass

    async def commit_updates(self):
        async with self._lock:
            # TODO: commit queued updates to #bot-database channel and update in memory db
            pass
