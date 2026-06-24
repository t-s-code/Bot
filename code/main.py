# main.py

from our_bot import OurBot
from models.config import *

def main():
    is_dry_run = True
    token = None

    config = BotConfig(
        channel_pruning_configs = [
            ChannelPruningConfig(
                channel_name="",
                channel_id=1,
                days_until_delete_messages_from_channel=3
            )
        ]
    )

    bot = Bot(is_dry_run, config)
    bot.run(token)


if __name__ == "__main__":
    main()
