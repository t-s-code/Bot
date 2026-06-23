## Project (File) Hierarchy
Below is a birds-eye view of the files which bring our bot to life.

```yaml

bot/

    README.md  # This file that you're reading now.

    LICENSE.md  # Says this whole bot & all its files are open source and free to use.

    requirements.txt # Tells Python, the language our bot runs on, which libraries we need in order to run our bot.

    main.py # The starting point of our application. A great place to look first if you want to try to get a feel for our code.

    core/ # The core utilities our bot needs to do its job well.

        __init__.py

        dry_run.py

        message_processor.py

    channels/ # These files help our bot read/write to the #bot-database and #bot-log channels.

        __init__.py

        database_channel.py

        log_channel.py

    jobs/

        __init__.py

        member_activity_job.py  # Converts members from active to inactive & vice-versa.

        channel_pruning_job.py # Deletes messages from channels that are older than we defined in the config

        channel_scanning_job.py # Scans messages from channels and updates database. Ensures we don't lose any member activity if Discord events are missed.
```

### Records in our `#bot-database` channel

These records store the bot’s memory and progress so it can safely restart. Without this database, the bot would lose _essential_ activity history when messages are pruned or deleted.

#### MEMBER_ACTIVITY_RECORD
Tracks when a member posted last.

```yaml
MEMBER_ACTIVITY_RECORD
user_id: <discord_user_id>
status: active | inactive
last_seen_message_at: <ISO_UTC_timestamp>
last_seen_message_id: <discord_message_id>
```

#### CHANNEL_SCANNING_CURSOR
Tracks how far our bot has scanned a channel for new messages.

```yaml
CHANNEL_SCANNING_CURSOR
channel_id: <discord_channel_id>
last_read_message_at: <ISO_UTC_timestamp>
last_read_message_id: <discord_message_id>
```

#### CHANNEL_PRUNING_CURSOR
Tracks how far our bot has gotten in deleting messages in a channel.

```yaml
CHANNEL_PRUNING_CURSOR
channel_id: <discord_channel_id>
last_checked_message_at: <ISO_UTC_timestamp>
last_checked_message_id: <discord_message_id>
```

### Timestamps
All timestamps are stored using **ISO 8601 UTC format**.

Example:
```
2026-02-03T19:42:00Z
```

Explanation:
- Date → `2026-02-03`
- Time → `19:42:00`
- `Z` means **UTC time (universal global time)**
