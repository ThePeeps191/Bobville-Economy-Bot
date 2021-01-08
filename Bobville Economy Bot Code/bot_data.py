'''
DATA FOR THE BOT
'''

# Import Discord
import discord

# Basic HelpSubcommand
@help.command(aliases=["p", "pro"])
async def profile(ctx):
	em = discord.Embed(title="Profile Command", description="Checks Your Profile", color=ctx.author.color)
	em.add_field(name="INFO", value="**Description**:\nChecks Your Game Profile\n\n**Syntax/Usage**:\n`?profile <optional member (mention them)>`\n\n**Cooldown**:\nNone\n\n**Aliases**:\n`p`, `pro`")
	await ctx.send(embed=em)
