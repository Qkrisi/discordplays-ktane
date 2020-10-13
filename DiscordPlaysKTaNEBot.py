from json import loads
from twitchio.ext import commands
import discord
import asyncio
import re

TwitchContext = None
DiscordChannel = None

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

EmojiOverrides = {}
TwitchOverrides = {}

ChannelID = -1
Nickname = ""
Oauth = ""
Prefix = ""
Channel = ""
BotToken = ""

with open("config.json", "r") as f:
	lines = f.readlines()
	for i in range(len(lines)):lines[i]=lines[i].strip()
	parsed = loads(''.join(lines))
	Oauth = parsed["TwitchToken"]
	BotToken = parsed["BotToken"]
	Nickname = parsed["Nickname"]
	Prefix = parsed["Prefix"]
	ChannelID = parsed["ChannelID"]
	Channel = parsed["TwitchChannel"]

def UpdateTwitchMessage(msg: str, members: list) -> str:
	rep = []
	for match in re.finditer("(\@(.*?)\#([0-9]{4}))", msg):
		for member in members:
			if member.name==match.groups()[1] and str(member.discriminator)==match.groups()[2]:
				rep.append((match.groups()[0], member.mention))
				break
	for emoji in EmojiOverrides:
		for match in re.finditer(f"(( |^)?{emoji}?( |$))", msg):
			m = list(match.groups())
			for key in range(len(m)):
				if m[key]==None:m[key]=""
			rep.append((m[0], f"{m[1]}{EmojiOverrides[emoji]}{m[2]}"))
	for replacement in rep:msg = msg.replace(replacement[0], replacement[1])
	return msg
	
def UpdateDiscordMessage(msg: str) -> str:
	for emoji in TwitchOverrides:msg = msg.replace(TwitchOverrides[emoji], f" {emoji} ")
	return msg

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(irc_token=Oauth, nick=Nickname, prefix=Prefix, initial_channels = [Channel])
		
	async def event_ready(self):
		print("Twitch bot ready!")
		
	async def event_message(self, message):
		if DiscordChannel!=None and message.author.name!=self.nick.lower():await DiscordChannel.send(f"[{message.author.name}] {UpdateTwitchMessage(message.content, DiscordChannel.members)}")
		await self.handle_commands(message)
		
	@commands.command(name='toggle')
	async def EnableDP(self, ctx):
		if not "broadcaster" in ctx.author.badges: return await ctx.send("Only the streamer can run this command!")
		global TwitchContext
		TwitchContext = ctx if TwitchContext==None else None
		await ctx.send(f"DiscordPlays is now {'enabled' if TwitchContext!=None else 'disabled'}!")

@client.event
async def on_ready():
	global DiscordChannel
	DiscordChannel = client.get_channel(ChannelID)
	for emoji in DiscordChannel.guild.emojis:
		EmojiOverrides[emoji.name] = f"<:{emoji.name[0]}:{emoji.id}>"
		TwitchOverrides[emoji.name] = f"<:{emoji.name}:{emoji.id}>"
	print("Discord bot ready!")
	print(f"Type {Prefix}toggle in Twitch chat to enable DiscordPlays!")

@client.event
async def on_message(message):
	if message.channel.id == ChannelID and TwitchContext!=None and message.author.id!=client.user.id: await TwitchContext.send(UpdateDiscordMessage(f"!runas {message.author.color} {message.author.name}#{message.author.discriminator} {message.content}" if message.content.startswith("!") else f"[{message.author.name}#{message.author.discriminator}] {message.content}"))

loop = asyncio.get_event_loop()
loop.create_task(Bot().start())
loop.create_task(client.start(BotToken))
loop.run_forever()
