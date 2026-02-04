# channels/config_channel.py

import discord


class ConfigChannel:
    """
    Handles reading and validating configuration from the #bot-config channel.

    When a moderator posts a new message in #bot-config
    - The latest message is parsed into a config object
    - If valid, the bot hot reloads using the new config
    - If invalid, the bot replies with a moderator-friendly error
    """

    def __init__(self, bot, config_channel_id):
        self._bot = bot
        self._config_channel_id = config_channel_id
        self._latest_valid_config = None

    async def get_config(self):
        """
        Returns the latest valid config.

        If not already cached, scans channel history until a valid
        config is found.
        """
        if self._latest_valid_config is not None:
            return self._latest_valid_config

        # TODO scan config channel history
        # TODO locate most recent valid config
        # TODO set self._latest_valid_config

        raise RuntimeError("No valid config found in config channel.")

    async def handle_possible_config_update(self, message):
        """
        Signal method called when any Discord message event occurs.

        If the message is in the config channel, attempt to load
        the latest config snapshot.
        """
        if message.channel.id != self._config_channel_id:
            return False

        if message.author.bot:
            return False

        await self.load_latest_config()
        return True

    async def load_latest_config(self):
        """
        Attempts to load config from the most recent moderator message.

        Does NOT scan backwards through history.

        If parsing succeeds:
            - Cache config
            - Trigger hot reload

        If parsing fails:
            - Reply to moderator with error message
        """

        # TODO fetch latest non-bot message in config channel
        # TODO attempt parse + validation
        # TODO update _latest_valid_config on success
        # TODO call self._bot.request_hot_reload()
        # TODO reply with moderator-friendly error on failure

        pass
