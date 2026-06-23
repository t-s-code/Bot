
## Records in our `#bot-database` channel

These records store the bot’s memory and progress so it can safely restart. This database enables our bot to:

- know a member is still active even if all their messages have been deleted
- restart without having to rescan everything from all channels
  
### MEMBER_ACTIVITY_RECORD
Tracks when a member posted last.

```yaml
MEMBER_ACTIVITY_RECORD
user_id: <discord_user_id>
status: active | inactive
last_seen_message_id: <discord_message_id>
last_seen_message_timestamp: <ISO_UTC_timestamp>
```

### CHANNEL_SCANNING_CURSOR
Tracks how far our bot has scanned a channel for new messages.

```yaml
CHANNEL_SCANNING_CURSOR
channel_id: <discord_channel_id>
last_scanned_message_id: <discord_message_id>
last_scanned_message_timestamp: <ISO_UTC_timestamp>
```

## Timestamps
All timestamps are stored using **ISO 8601 UTC format**.

Example:
```
2026-02-03T19:42:00Z
```

Explanation:
- Date → `2026-02-03`
- Time → `19:42:00`
- `Z` means **UTC time (universal global time)**
