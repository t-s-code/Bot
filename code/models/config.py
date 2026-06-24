# models/config.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class BotConfig:
    channel_pruning_configs: list[ChannelPruningConfig]


@dataclass(frozen=True)
class ChannelPruningConfig:
    channel_name: str
    channel_id: int
    days_until_delete_messages_from_channel: int

bot_config = BotConfig(
    channel_pruning_configs = [
        ChannelPruningConfig(
            channel_name="",
            channel_id=1,
            days_until_delete_messages_from_channel=3
        )
    ]
)
