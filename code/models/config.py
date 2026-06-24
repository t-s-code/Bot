# models/config.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    channel_pruning_configs: list[ChannelPruningConfig]


@dataclass(frozen=True)
class ChannelPruningConfig:
    channel_name: str
    channel_id: int
    days_until_delete_messages: int
