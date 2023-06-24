# Rust Wipe Bot

Discord Bot that allows users to add and remove their favourite Rust servers to be notified of the exact time they wipe. ID from BattleMetrics is used.

![battleurl](https://github.com/Ryan-RH/RustWipeBot/assets/108598537/eda2c3f0-c7b3-4449-bb38-876c67f7c3c2)

![add remove](https://github.com/Ryan-RH/RustWipeBot/assets/108598537/ab5ebb75-2503-4807-8ebf-4e612f1a79f5)

?serverlist can be used to see what servers that have been added with their corresponding ID.

![serverlist](https://github.com/Ryan-RH/RustWipeBot/assets/108598537/dc3ff7ca-2c28-425f-ad0b-74dc20c2ce37)

When a server wipes, an embed will be posted, which is regularly edited to show the current population and time since the last wipe.

![justwiped](https://github.com/Ryan-RH/RustWipeBot/assets/108598537/9c2b69a3-dc87-4536-ba24-7e84f5d0e499)

When the bot is activated, and after each UTC day, the channel supplied by channel_id will be purged.

# Important

- Discord Token needs to be added. 

- Create a notepad document with server ids called serverids.txt. If you manually add server IDs to Notepad, make sure to add a new line after the last entered ID.

- Change channel_id to a specific channel in which wipe embeds will be posted, commands should be executed in a separate channel

- Packages required: discord.py, pytz

# Possible Problems

- Crashes when another user, other than the bot, posts in the specified channel

- Possible crash if attempt to remove server while serverlist command posted

- If ?add [id] is spammed, program will be rate-limited and therefore crash

# Future Additions

- Rust Map

- ?pop command
