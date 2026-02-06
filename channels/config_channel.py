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
        - Locate the last success message written by the bot
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
    # Parsing 
    # -------------------------

    def _parse_config(self, message_text):
        """
        Creates a Config object from a message like:
        
        ```
        # Bot Config
        Please read the following link before updating our bot's config: TODO LINK.
        
        ━━━━━━━━━━━━━━━━
        
        ## Channel Pruning
        
        - #introductions = 30 days
        - #chat = 7 days
        
        ━━━━━━━━━━━━━━━━
        
        ## Member Inactivity
        
        - Active role = @Active
        - Inactive role = @Inactive
        - Days until inactive = 30 days
        ```
        """
        # TODO split message_text into individual lines
        
        # TODO normalize lines
        #   - strip whitespace
        #   - ignore lines that are not either
        #      - (a) a markdown heading
        #      - or (b) a markdown bullet item
        #      - Examples of ignored lines: whitespace lines, decorative lines, paragraphs (comments)
        #      - Throw if there are any code block lines or html lines (these could easily break this simple parser)

        # TODO locate line indicies for expected headings
        #   - heading like: "# Our Bot's Config"
        #   - heading like: "## Channel Pruning"
        #   - heading like: "## Member Inactivity"
        #   - Throw if any other headings are discovered

        # TODO use section heading indicies to group lines per section

        # TODO parse each markdown bullet from each section into tuples
        #   - expect format: "- STRING_1 = STRING_2" (ignore extra whitespace)
        #   - result: list of (STRING_1, STRING_2)
        #   - Throw if there are any other lines in the section (should have been handled by normalization)
        
        # TODO parse Channel Pruning's tuples into List[ChannelPruningPolicy]

        # TODO Member Activity's tuples into MemberActivityPolicy
        
        # TODO construct Config object from parsed sections

        # TODO return Config
        pass

    def _parse_channel_pruning_policy(self, policy_tuple):
        # TODO: parse channel pruning policy tuple into dataclass
        #   - extract channel mention (#channel) from first element
        #   - extract N as integer from second element (expected format: "N days" or "N day")
        #   - resolve channel mention → channel_id + channel_name
        #   - construct ChannelPruningPolicy object

        # TODO return ChannelPruningPolicy
        pass

    def _parse_member_activity_policy(self, policy_tuple):
        #   - enforce required field ordering
        #   - parse roles and days values
        
        # TODO return MemberActivityPolicy
        pass

    # -------------------------
    # Validation
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
            except Exception as e:
                raise ValueError(
                    f"Encountered error while parsing the ChannelPruningPolicy for channel_id={policy.channel_id} (channel_name={policy.channel_name})."
                ) from e

        # Validate uniqueness of channel_id across policies
        seen = set()
        for policy in channel_pruning_policies:
            if policy.channel_id in seen:
                raise ValueError(
                    f"There was more than one ChannelPruningPolicy defined for channel_id={policy.channel_id} (channel_name={policy.channel_name})."
                )
            seen.add(policy.channel_id)

    def _validate_channel_pruning_policy(self, channel_pruning_policy):
        if channel_pruning_policy.channel_id <= 0:
            raise ValueError(
                f"Invalid channel_id={channel_pruning_policy.channel_id}. Expected a positive number."
            )

        if channel_pruning_policy.delete_older_than_days <= 0:
            raise ValueError(
                f"Invalid delete_older_than_days={channel_pruning_policy.delete_older_than_days}. Please specify a number greater than 0."
            )
