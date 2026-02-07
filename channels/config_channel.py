# channels/config_channel.py

from dataclasses import dataclass
from enum import Enum, auto

import discord


class ConfigChannel:
    """
    Handles reading and validating configuration from the #bot-config channel.

    When a moderator posts a new message in #bot-config
    - The latest message is parsed into a config object
    - If valid, the bot hot reloads using the new config and posts a success message in this channel
    - If invalid, the bot replies with a moderator-friendly error
    """

    def __init__(self, bot, discord_client, config_channel_id):
        self._bot = bot
        self._discord_client = discord_client
        self._config_parser = _ConfigParser(discord_client)
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

class _ConfigParser:
    """
    Responsible for converting raw config message text into Config objects.
    """

    # -------------------------
    # Section Constants
    # -------------------------

    SECTION_ROOT = "our bot config"
    SECTION_CHANNEL_PRUNING = "channel pruning"
    SECTION_MEMBER_INACTIVITY = "member inactivity"

    REQUIRED_SECTIONS = {
        SECTION_ROOT,
        SECTION_CHANNEL_PRUNING,
        SECTION_MEMBER_INACTIVITY,
    }

    # Member inactivity expected fields (normalized keys)
    MEMBER_ACTIVITY_FIELDS = {
        "active role",
        "inactive role",
        "days until inactive",
    }

    def __init__(self, discord_client):
        self._discord_client = discord_client

    def parse(self, message_text):
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
        #   - Preserve original line numbers for error reporting

        # TODO normalize lines into a simplified representation
        #   - strip whitespace
        #   - ignore lines that are not either:
        #       (a) markdown heading
        #       (b) markdown bullet item (supports "-" and "*")
        #   - treat headings case-insensitively
        #   - treat heading level (#, ##, ###, etc.) as irrelevant
        #   - Throw if any code block markers (```) or html-like tags (<...>) are found

        # TODO build section map
        #   - Create dict[section name, List[normalized line in section]]
        #
        #   Requirements:
        #       - Normalize section names to lowercase
        #       - Heading level (# vs ## etc.) is ignored
        #       - Throw if:
        #           * duplicate section appears
        #           * unknown section appears
        #           * any required section is missing

        # TODO parse bullet lines into tuples
        #   - expect format: "- STRING_1 = STRING_2" OR "* STRING_1 = STRING_2"
        #   - split on FIRST "=" only
        #   - ignore extra whitespace around "="
        #   - output: List[ParsedBullet] = List[(normalized line, key, value)]
        #   - Throw if bullet does not match expected format

        # TODO parse Channel Pruning section

        # TODO parse Member Inactivity section

        # TODO construct Config object from parsed sections

        # TODO return Config
        pass

    # -------------------------
    # Section Parsers
    # -------------------------

    def _parse_channel_pruning_section(self, parsed_bullets):
        """
        Converts parsed bullets into List[ChannelPruningPolicy]
        """

        # For each tuple:

        #    TODO extract channel mention (<#channel_id>) from key
        #    TODO extract N as reminder days integer from value
        #      - Accept "N day" or "N days" (case-insensitive)

        #    TODO resolve channel mention -> channel_id + channel_name using discord client

        #    TODO construct ChannelPruningPolicy

        # TODO return List[ChannelPruningPolicy]
        pass

    def _parse_member_activity_section(self, policy_tuples):
        """
        Converts parsed bullets into MemberActivityPolicy
        """

        # TODO convert tuples into dictionary:
        #   normalized_field_name -> (value, normalized line)

        #   Field normalization rules:
        #       - lowercase
        #       - collapse extra whitespace
        #       Example:
        #           "Active   Role" -> "active role"

        # TODO validate:
        #   - all required fields exist
        #   - no unknown fields exist

        # TODO parse:
        #   - role mentions -> role_id + role_name
        #   - days value -> integer (accept "N day(s)")

        # TODO construct MemberActivityPolicy

        # TODO return MemberActivityPolicy
        pass

class _LineType(Enum):
    HEADING = auto()
    BULLET = auto()

@dataclass(frozen=True)
class _NormalizedLine:
    raw_text: str
    line_number: int
    line_type: _LineType
    normalized_text: str
