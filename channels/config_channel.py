# channels/config_channel.py

from dataclasses import dataclass
from enum import Enum, auto
import re

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


# --------------------------------
# Helpers
# --------------------------------

class _ParseError(ValueError):
    def __init__(self, message: str, line_num: int, raw_text: str):
        super().__init__(message)
        self.line_num = line_num
        self.raw_text = raw_text
    def __str__(self):
        return f"{super().__str__()} (line {self.line_num}: {self.raw_text})"
    
class _LineType(Enum):
    HEADING = auto()
    BULLET = auto()

@dataclass(frozen=True)
class _NormalizedLine:
    raw_text: str
    line_number: int
    line_type: _LineType
    normalized_text: str

class _SectionHeading(Enum):
    ROOT = "Our Bot Config"
    CHANNEL_PRUNING = "Channel Pruning"
    MEMBER_INACTIVITY = "Member Inactivity"

    def __init__(self, display_name):
        self.display_name = display_name
        self.normalized_name = display_name.lower()

    @classmethod
    def from_normalized(cls, normalized_name):
        for section in cls:
            if section.normalized_name == normalized_name:
                return section
        return None

    @classmethod
    def display_names(cls):
        return [section.display_name for section in cls]




class _ConfigParser:
    """
    Converts raw config message text into Config objects.
    """

    HTML_LIKE_PATTERN = re.compile(r"<[^>]+>")

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

        raw_lines = message_text.splitlines()
        normalized_lines = self._normalize_lines(raw_lines)

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

    def _normalize_lines(self, raw_lines):
        normalized_lines = []

        for line_num, raw_line in enumerate(raw_lines, start=1):
            stripped_text = raw_line.strip()

            if not stripped_text:
                continue # ignore lines that are empty or purely whitespace

            if stripped_text.startswith("```"):
                raise _ParseError(
                    "Code blocks (```) are not allowed.",
                    line_num,
                    raw_line
                )

            if self.HTML_LIKE_PATTERN.search(stripped_text):
                raise _ParseError(
                    "HTML tags are not allowed.",
                    line_num,
                    raw_line
                )

            line_type = None
            normalized_text = None

            if stripped_text.startswith("#"):
                line_type = _LineType.HEADING
                normalized_text = stripped_text.strip("# ").strip().lower()

            elif stripped_text.startswith("-") or stripped_text.startswith("*"):
                line_type = _LineType.BULLET
                normalized_text = stripped_text[1:].strip()

            else:
                # Ignore all other lines (comments, decorative lines, paragraphs, etc.)
                pass

            if line_type is not None:
                normalized_lines.append(
                    _NormalizedLine(
                        raw_text=raw_line,
                        line_number=line_num,
                        line_type=line_type,
                        normalized_text=normalized_text,
                    )
                )

        return normalized_lines

    def _build_section_map(self, normalized_lines):
        """
        Build a map of _SectionHeading -> list[NormalizedLine]
        Ensure all headings are present that should be present.
        Ensure no additional headings are present.
        """
        section_map = {}
        current_section = None

        for line in normalized_lines:

            if line.line_type == _LineType.HEADING:
                section = _SectionHeading.from_normalized(line.normalized_text)

                if section is None:
                    raise _ParseError(
                        f'Unexpected section: "{line.normalized_text}". '
                        f'Expected one of: {", ".join(_SectionHeading.display_names())}.',
                        line.line_number,
                        line.raw_text
                    )

                if section in section_map:
                    raise _ParseError(
                        f'Duplicate section: "{section.display_name}". '
                        'Please only define each section once.',
                        line.line_number,
                        line.raw_text
                    )

                current_section = section
                section_map[section] = []

            elif line.line_type == _LineType.BULLET:
                if current_section is None:
                    # Ignore bullets before the first section.
                    pass
                else:
                    section_map[current_section].append(line)

        required_sections = set(_SectionHeading.values())
        missing_sections = required_sections - set(section_map.keys())

        if missing_sections:
            missing_section_names = [
                section.display_name
                for section in _SectionHeading.values()
                if section not in section_map
            ]

            raise _ParseError(
                f'Missing required section(s): {", ".join(missing_section_names)}.',
                -1,
                "N/A"
            )

        return section_map

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
