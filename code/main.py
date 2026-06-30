# main.py

import os, sys
from our_bot import OurBot
from models.config import BotConfig, ChannelPruningConfig, ChannelScanningConfig

def main():
    is_dry_run = True
    discord_api_token = os.environ.get("DISCORD_API_TOKEN", None)
    if discord_api_token is None:
        raise ValueError("DISCORD_API_TOKEN environment variable must be set.")


    config = BotConfig(
        server_id = -1,
        channel_scanning_config = ChannelScanningConfig(
            minutes_between_scans = 5
        ),
        channel_pruning_configs = [
            ChannelPruningConfig(
                channel_name="Rules",
                channel_id=1356995099598389338,
                days_until_delete_messages_from_channel=3,
            )
        ]
    )

    bot = OurBot(is_dry_run, config)
    bot.run(discord_api_token)


if __name__ == "__main__":
    main()
