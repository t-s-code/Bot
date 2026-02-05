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

    # -------------------------
    # Validation Logic
    # -------------------------

    def _validate_config(self, config):
        """
        Throws if the config object is not valid.

        Prevents trivial mistakes in configs from being loaded.

        Gives useful error messages for moderators when validation fails.
        """

        self._validate_channel_pruning_policies(
            config.channel_pruning_policies
        )

    def _validate_channel_pruning_policies(self, channel_pruning_policies):
        for policy in channel_pruning_policies:
            try:
                self._validate_channel_pruning_policy(policy)
            except e:
                raise ValueError(
                    f"Encountered error while parsing the ChannelPruningPolicy for channel_id={policy.channel_id}",
                    e
                )

        # Validate uniqueness of channel_id across policies
        unique_channel_ids = set(policy.channel_id for policy in channel_pruning_policies)
        if len(channel_pruning_policies) != len(unique_channel_ids):
            duplicate_channel_id = channel_pruning_policies.remove_all(unique_channel_ids).first()
            raise ValueError(
                f"There was more than one ChannelPruningPolicy defined for channel_id={duplicate_channel_id}"
            )

    def _validate_channel_pruning_policy(self, channel_pruning_policy):
        if channel_pruning_policy.channel_id <= 0:
            raise ValueError(
                f"Invalid channel_id={channel_pruning_policy.channel_id}. Expected a positive number."
            )

        if channel_pruning_policy.delete_older_than_days <= 0:
            raise ValueError(
                f"Invalid delete_older_than_days={channel_pruning_policy.delete_older_than_days}. Please specify a number greater than 0."
            )
