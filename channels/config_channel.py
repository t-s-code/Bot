# channels/config_channel.py

import discord


class ConfigChannel:
    """
    Handles reading and validating configuration from the #bot-config channel.

    When a moderator posts a new message in #bot-config
    - The latest message is parsed into a config object
    - If valid, the bot hot reloads using the new config and posts a success message in this channel
    - If invalid, the bot replies with a moderator-friendly error
    """

    def __init__(self, bot, config_channel_id):
        self._bot = bot
        self._config_channel_id = config_channel_id
        self._latest_valid_config = None

    async def get_config(self):
        """
        Returns the config that was most recently active.

        If this bot is starting up:
        - Scan config channel history
        - Locate the last success message writen by the bot
        - Load the config from the message linked to by the success message
        - If there are no success messages in the channel, try loading the config from the last message not authored by a bot
        
        If the bot is already running:
        - Return the config that is currently in use
        """

        if self._latest_valid_config is not None:
            return self._latest_valid_config

        # TODO scan config channel history for latest success message
        # TODO load the config from the message that is linked to
        # TODO load the config from the last message not written by a bot, if there were no success messages in the channel
        # TODO parse config message into config object

        config = None  # placeholder for parsed config

        self._validate_config(config)

        self._latest_valid_config = config
        return config

    async def handle_possible_config_update(self, message):
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

    # Validation Logic
    
    def _validate_config(self, config):
        """
        Throws if the config object is not valid.

        Prevents trivial mistakes in configs from being loaded.

        Gives useful error messages for moderators when validation fails.
        """
        pass

    def _validate_channel_prunning_policies(self, channel_prunning_policies):
        # TODO validate channel_prunning_policies.channel_id is unique
        pass
    
    def _validate_channel_prunning_policy(self, channel_prunning_policy):
        # TODO validate channel_id is a positive number
        # TODO validate delete_older_than_days is a postive number
        pass
