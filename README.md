# About Our Bot

Our bot helps us have a community that is more conducive for peer support.

Our bot:

- Deletes messages from certain channels when they get too old. This keeps our channels feeling cozier for peer support and connection.

- Marks members as inactive when they haven't posted in a while, and marks inactive members as active whenever they post. The internet is never fully safe. However limiting our rooms to only people who are participating helps our rooms feel a little easier to connect in.
---

# Technical Stuff
This section contains stuff that may help you understand our code if you try to read it. Feel free to skim it and ask questions if you'd like! Also, feel free not to read it 😂

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

#### MEMBER_ACTIVITY
Tracks each member’s last known activity and role state.

```yaml
MEMBER_ACTIVITY
user_id: <discord_user_id>
status: active | inactive
last_seen_at: <ISO_UTC_timestamp>
last_seen_message_id: <discord_message_id>
```

#### CHANNEL_SCANNING_CURSOR
Tracks how far the bot has processed messages within a channel.  This prevents the bot from re-reading old messages after restarting.

```yaml
CHANNEL_SCANNING_CURSOR
channel_id: <discord_channel_id>
last_read_message_id: <discord_message_id>
last_read_at: <ISO_UTC_timestamp>
```

#### CHANNEL_PRUNING_CURSOR
Tracks how far the bot has checked messages for deletion in a channel.  This helps the bot avoid scanning the same messages repeatedly.

```yaml
CHANNEL_PRUNING_CURSOR
channel_id: <discord_channel_id>
last_checked_message_id: <discord_message_id>
last_checked_at: <ISO_UTC_timestamp>
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
