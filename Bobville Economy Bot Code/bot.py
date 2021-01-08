# Import The Discord Modules
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.cooldowns import BucketType

# Import The Other Modules
import os
import json
import random
import math
from itertools import cycle

# Import My Custom Modules
from trivia import Trivia
import trivia

# Make The Bot Object
client = commands.Bot(command_prefix="?")
# Remove The Default Help Command
# So We Can Make A Better Help Command
client.remove_command("help")

# Load The Bank JSON File
with open("bank.json") as f:
	bank = json.load(f)

# Make A Function That Dumps The Bank Dict # Into The JSON File
def save_bank():
	with open('bank.json', 'w') as f:
		json.dump(bank, f)

# A Function That Creates A Bank Account
# For A User, If They Don't Have One
def account(id):
	id = str(id)
	have_id = id in bank
	if not have_id:
		bank[id] = 0
	save_bank()

# Create The Salary Loop
# Adds The Salary Every Minute
@tasks.loop(seconds=60)
async def add_salary():
	pass

# The Bot on_ready Event
@client.event
async def on_ready():
	#add_salary.start()
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For ?help"))
	print(f"{client.user} Is Ready")

# The Bot on_message Event
@client.event
async def on_message(msg):
	m = msg.content
	m = m.lower()
	account(msg.author.id)
	# Reactions
	if "coin" in m:
		await msg.add_reaction("🪙")
	# Converts The Message Into Lowercase
	msg.content = m
	# Only Does The Command If The Sender
	# Is Not A Bot
	if not msg.author.bot:
		await client.process_commands(msg)

# Command Error Handler
@client.event
async def on_command_error(ctx, error):
	# Command Not Found
	if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title="Invalid Command", description=f"{str(error)}. Try `?help` for a list of commands.", color=ctx.author.color)
		await ctx.send(embed=em)

# Profile Command
@client.command(aliases=["p", "pro"])
async def profile(ctx, user:discord.Member):
	account(user.id)
	em = discord.Embed(title=f"{user.name}'s Profile", description=f"{user.mention}'s Game Stats:", color=ctx.author.color)
	author_coins = bank[str(user.id)]
	em.add_field(name="Coins", value=f"**{author_coins} Bobcoins:coin:**")
	em.set_thumbnail(url=user.avatar_url)
	save_bank()
	await ctx.send(embed=em)
@profile.error
async def profile_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		em = discord.Embed(title=f"{ctx.author.name}'s Profile", description=f"{ctx.author.mention}'s Game Stats:", color=ctx.author.color)
		author_coins = bank[str(ctx.author.id)]
		em.add_field(name="Coins", value=f"**{author_coins} Bobcoins:coin:**")
		em.set_thumbnail(url=ctx.author.avatar_url)
		save_bank()
		await ctx.send(embed=em)

# Work Command
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(ctx):
	bank[str(ctx.author.id)] += 20
	save_bank()
	em = discord.Embed(title="Work", description=f"You went to work! Your boss payed you **20 Bobcoins:coin:**.\nCurrent Balance: **{bank[str(ctx.author.id)]} Bobcoins:coin:**", color=ctx.author.color)
	await ctx.send(embed=em)
# Work Cooldown Error
@work.error
async def work_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		em = discord.Embed(title="Command Is On Cooldown", description=f"Oops! Looks Like You Have Already Gained Some Coins. Please Wait **{round(error.retry_after, 1)}** Seconds Before Using `?work` Again.", color=ctx.author.color)
		await ctx.send(embed=em)

# Beg Command
@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def beg(ctx):
	g = random.randint(2, 30)
	bank[str(ctx.author.id)] += g
	save_bank()
	em = discord.Embed(title="Beg", description=f"Here Are **{g}** Bobcoins:coin:!\nCurrent Balance: **{bank[str(ctx.author.id)]} Bobcoins:coin:**", color=ctx.author.color)
	await ctx.send(embed=em)
# Beg Cooldown
@beg.error
async def beg_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		em = discord.Embed(title="Command Is On Cooldown", description=f"Oops! Looks Like You Have Already Begged. Please Wait **{round(error.retry_after, 1)}** Seconds Before Using `?beg` Again.", color=ctx.author.color)
		await ctx.send(embed=em)

# Bot-Info Command
@client.command(aliases=["bot-info"])
async def bot_info(ctx):
	em = discord.Embed(title="Info", description="**I Was Made By The_Peeps191#5993, And I Am A Game Bot.**\n*Links:*\n- [GitHub](https://github.com/ThePeeps191)\n- [Repl.it](https://repl.it/@ThePeeps191)\n- [YouTube](https://www.youtube.com/channel/UCjsJxOviseq9xQNrVUIDC1A)\n- [My Source Code](https://github.com/ThePeeps191/Bobville-Economy-Bot)", color=ctx.author.color)
	await ctx.send(embed=em)

# Help Command
@client.group(invoke_without_command=True)
async def help(ctx):
	em = discord.Embed(title="Help", description="You Can Use `?help <command>` If You Want Specific Information On A Command. You Can Also [Go To Our Help Server](https://discord.gg/H3YCkQaxQJ).", color=ctx.author.color)
	em.add_field(name="Categorys", value="`?help gameplay`  |  `?help non-gameplay`")
	await ctx.send(embed=em)

# Non-Gameplay Help Commands
@help.command(aliases=["non-gameplay"])
async def non_gameplay(ctx):
	em = discord.Embed(title="Non-Gameplay Commands", description="The Commands that Are Not For The Gamelay Itself. Use `?help <command>` For Information On A Command", color=ctx.author.color)
	em.add_field(name="Commands", value="`bot-info`")
	await ctx.send(embed=em)

@help.command(aliases=["bot-info"])
async def bot_info(ctx):
	em = discord.Embed(title="Bot-Info Command", description="Shows You Information On The Bot", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nShows You Information On The Bot.\n\n**Syntax/Usage**:\n`?profile bot-info`\n\n**Cooldown**:\nNone\n\n**Aliases**:\nNone")
	await ctx.send(embed=em)

# Gameplay Help Commands
@help.command()
async def gameplay(ctx):
	em = discord.Embed(title="Gameplay Commands", description="The Commands For The Game. Use `?help <command>` For Information On A Command", color=ctx.author.color)
	em.add_field(name="Commands", value="`help`, `work`, `profile`, `beg`")
	await ctx.send(embed=em)

@help.command(aliases=["p", "pro"])
async def profile(ctx):
	em = discord.Embed(title="Profile Command", description="Checks Your Profile", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nChecks Your Game Profile\n\n**Syntax/Usage**:\n`?profile <optional member (mention them)>`\n\n**Cooldown**:\nNone\n\n**Aliases**:\n`p`, `pro`")
	await ctx.send(embed=em)

@help.command()
async def beg(ctx):
	em = discord.Embed(title="Beg Command", description="Makes You Beg", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nMakes You Beg. You Will Earn 2-30 Bobcoins:coin:.\n\n**Syntax/Usage**:\n`?beg`\n\n**Cooldown**:\n20 Seconds\n\n**Aliases**:\nNone")
	await ctx.send(embed=em)

@help.command()
async def work(ctx):
	em = discord.Embed(title="Work Command", description="Makes You Earn Coins", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nMakes You Work\n\n**Syntax/Usage**:\n`?work`\n\n**Cooldown**:\n30 Seconds\n\n**Aliases**:\nNone")
	await ctx.send(embed=em)

@help.command()
async def help(ctx):
	em = discord.Embed(title="Help Command", description="Shows You The Commands", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nInformation On The Commands.\n\n**Syntax/Usage**:\n`?help`\n\n**Cooldown**:\nNone\n\n**Aliases**:\nNone")
	await ctx.send(embed=em)




BOT_TOKEN = os.getenv("TOKEN") 
client.run(BOT_TOKEN)
