# models/config.py

from dataclasses import dataclass


@dataclass(frozen=True)
class BotConfig:
    channel_pruning_configs: list[ChannelPruningConfig]
    
    def validate(self):
        seen_ids = set()
        
        for c in self.channel_pruning_configs:
            seen_ids.add(c.channel_id)
            c.validate()

        if len(seen_ids) != len(self.channel_pruning_configs):
            raise ValueError("Every channel_id in channel_pruning_configs must be unique")

@dataclass(frozen=True)
class ChannelPruningConfig:
    channel_name: str
    channel_id: int
    days_until_delete_messages_from_channel: int

    def validate(self):
        if self.days_until_delete_messages_from_channel < 1:
            raise ValueError("days_until_delete_messages_from_channel must be > 0")
