# jobs/channel_scanning_job.py

import asyncio

class ChannelScanningJob:

    def __init__(self, discord_client, database, config):
        self._discord_client = discord_client
        self._database = database
        self._config = config

    async def run(self):
        print("Scan Job started")
        while True:
            await self.scan_all_channels()
            await asyncio.sleep(self._config.channel_scanning_config.minutes_between_scans * 60)

    async def scan_all_channels(self):
        for channel_pruning_config in self._config.channel_pruning_configs:
            cursor, member_activity_records = await self.scan_channel(channel_pruning_config)
            self._database.queue_update(cursor)
            for record in member_activity_records:
                self._database.queue_update(record)
        await self._database.commit_updates()

    async def scan_channel(self, channel_pruning_config):
        cursor = await self._database.get_channel_scanning_cursor(channel_pruning_config.channel_id)
        member_messages = await self.scan_channel_from_cursor(cursor)
        member_activity_records = self._convert_to_member_activity_records(member_messages)
        updated_cursor = self._create_updated_cursor(cursor, member_messages)
        return (updated_cursor, member_activity_records)

    async def scan_channel_from_cursor(self, cursor):
        # TODO: scan messages directly in the channel for now, we will handle threads later.
        return []

    def _convert_to_member_activity_records(self, messages):
        # TODO: convert messages to member activity records
        return []

    def _create_updated_cursor(self, old_cursor, messages):
        # TODO: create updated cursor with last scanned message info
        pass
