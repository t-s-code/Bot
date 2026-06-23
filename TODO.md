## 🏗️ Implement: Scan all channels (& threads)
- Scan all channels specified in config on startup and periodically (for missed events)
- Need existing cursor per room, if it exists 
- Add pending changes to MemberActivity and ChannelScanningCursor records
- Commit changes when done 
- Stub DB as needed

## 🏗️ Implement: Database
- In memory snapshot of member activity and cursors
- Initialize from DB channel
- Queue pending changes to DB in queue
- Commit: Lock DB, write pending changes to channel and in memory DB, unlock DB

## 🏗️ Implement: Scan channel on message event

## 🏗️ Implement: Prune messages from channels
- For each configured room, delete messages older than retention period

## 🪨 Milestone: Feature Parity!
Replace existing Bot! 🥳

## 🏗️ Implement: Pruning for threads

## 🏗️ Implement: Member -> Inactive Member

## 🏗️ Implement: Inactive Member -> Member

## 🏗️ Implement: Delete inactive threads

## 🪨 Milestone: No Manual Roles
