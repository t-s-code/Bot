## 🏗️ Implement: Scan all channels (& threads)
ScanChannelsJob.scanAllChannels()
- (memberActivityRecords, channelScanningCursors) = (self.scanChannel(channelId) for scanChannelConfig in config).flatten()
- database.queueUpdate(r) for r in memberActivityRecords
- database.queueUpdate(c) for c in channelScanningCursors
- database.commitUpdates()

ScanChannelsJob.scanChannel(channelId)
- cursor = database.getChannelScanningCursor()
- memberMessages = self.scanFromCursor(cursor)
- updatedCursor = Cursor(memberMessages.last())
- return (memberActivityRecords, cursor)

ScanChannelsJob.scanChannelFromCursor(cursor)
- client.scanUntilEnd(cursor.lastMessageId)
- return messagesScanned

Bot.run()
- discord.login()

Bot.onReady()
- database.load()
- scanChannelsJob.scanAllChannels()
- Launch Task: self.periodicUpdate()

Bot.periodicUpdate()
  - scanChannelsJob.scanAllChannels()
  - Launch Task: self.periodicUpdate()

Database.load()
- self.lock()
- dbMessages = discordClient.readAllMessages(#bot-database)
- self.instantiate(dbMessages)
- self.unlock()

Database.instantiate(discordMessages)

Database.getChannelScanningCursor(channelId): ChannelScanningCursor?

Database.getMemberActivity(memberId)

Database.queueUpdate(ChannelScanningCursor | MemberActivity)

Database.commitUpdates()
- self.lock()
- update/create messages in channel
- update/create records in memory
- self.unlock()


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
