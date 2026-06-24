# main.py

"""
Application entry point.

Responsibilities:
- Initialize Discord client
- Wire services and jobs together
- Schedule high level bot workflows
"""

import asyncio
import discord

from core.dry_run import DryRun
from core.message_processor import MessageProcessor

from channels.database_channel import DatabaseChannel
from channels.log_channel import LogChannel

from jobs.channel_scanning_job import ChannelScanningJob


def main():
    is_dry_run = None
    token = None

    bot = Bot(is_dry_run)
    bot.run(token)


if __name__ == "__main__":
    main()
