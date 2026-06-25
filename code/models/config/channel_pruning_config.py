# models/config/channel_pruning_config.py

from dataclasses import dataclass

@dataclass(frozen=True)
class ChannelPruningConfig:
    channel_name: str
    channel_id: int
    days_until_delete_messages_from_channel: int

    def validate(self):
        if self.days_until_delete_messages_from_channel < 1:
            raise ValueError("days_until_delete_messages_from_channel must be > 0")
