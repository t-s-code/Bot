# models/database/channel_scanning_cursor.py

from dataclasses import dataclass
from datetime import datetime
from typing import List

from .thread_scanning_cursor import ThreadScanningCursor

@dataclass(frozen=True)
class ChannelScanningCursor:
    channel_id: int
    last_scanned_message_id: int
    last_scanned_message_timestamp: datetime
    thread_scanning_cursors: List[ThreadScanningCursor]
