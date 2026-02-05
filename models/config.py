# models/config.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    channel_pruning_policies: list[ChannelPruningPolicy]


@dataclass(frozen=True)
class ChannelPruningPolicy:
    channel_name: str
    channel_id: int
    delete_older_than_days: int
