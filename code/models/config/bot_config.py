# models/config/bot_config.py

from dataclasses import dataclass
from typing import List

from .channel_pruning_config import ChannelPruningConfig

@dataclass(frozen=True)
class BotConfig:
    channel_pruning_configs: List[ChannelPruningConfig]
    
    def validate(self):
        seen_ids = set()
        
        for c in self.channel_pruning_configs:
            seen_ids.add(c.channel_id)
            c.validate()

        if len(seen_ids) != len(self.channel_pruning_configs):
            raise ValueError("Every channel_id in channel_pruning_configs must be unique")
