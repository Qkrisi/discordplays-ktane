# DiscordPlays:KTaNE Bot

The synchronizes the chat of a Twitch channel with a discord channel, an handles TP commands.

## Dependencies

-[Python 3.7+](https://www.python.org/downloads/)

-[twitchio](https://pypi.org/project/twitchio/)

-[discord.py](https://pypi.org/project/discord.py/)

## Run

To run the bot, create a config.json with the following properties:

```json
{
	"TwitchToken":"<oauth token>",
	"BotToken":"<Discord bot token>",
	"Nickname":"<twitch bot nickname>",
	"Prefix":"<twitch prefix>",
	"ChannelID":<Discord channel ID>,
	"TwitchChannel":"<twitch channel>"
}
```

| Name | Description |
| --- | --- |
| TwitchToken | Oauth token of the bot ([Get the token here](https://twitchapps.com/tmi/)) |
| BotToken | Token of the Discord bot |
| Nickname | The name of the Twitch bot |
| Prefix | Prefix to use commands with on Twitch |
| ChannelID| The identifier of the Discord channel (integer) |
| TwitchChannel | The name of the Twitch channel the bot should join to |
