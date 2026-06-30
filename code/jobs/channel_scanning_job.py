# jobs/channel_scanning_job.py

import asyncio

from models.database.member_activity import MemberActivityRecord, MemberActivityStatus

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
        member_messages = await self._scan_channel_from_cursor(channel_pruning_config.channel_id, cursor)
        member_activity_records = self._convert_to_member_activity_records(member_messages)
        print("Calculated records:")
        for record in member_activity_records:
            print(record)
        updated_cursor = self._create_updated_cursor(cursor, member_messages)
        return (updated_cursor, member_activity_records)

    async def _scan_channel_from_cursor(self, channel_id, cursor):
        channel = self._discord_client.get_channel(channel_id)
        if not channel:
            raise ValueError(f"Our bot does not have access to channel_id={channel_id}")

        if cursor is not None:
            raise NotImplemented("scanning from cursor")

        messages = []
        async for message in channel.history(limit=None, oldest_first=True):
            messages.append(message)

        category = f"{channel.category.name}: " if channel.category else ""
        print(f"Finished scanning {category}{channel.name} ({channel.id})")

        return messages

    def _convert_to_member_activity_records(self, messages):
        record_by_user_id = dict()

        for message in messages:
            uid = message.author.id
            if uid in record_by_user_id:
                record = record_by_user_id[uid].replace_with_latest_message(message)
            else:
                record = MemberActivityRecord.create_from_message(message)
            record_by_user_id[uid] = record

        return record_by_user_id.values()

    def _create_updated_cursor(self, old_cursor, messages):
        # TODO: create updated cursor with last scanned message info
        pass
