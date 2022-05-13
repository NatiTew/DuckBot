import discord
from discord.ext import commands
from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
client = commands.Bot(command_prefix = "!")
slash = SlashCommand(client, sync_commands=True)

@slash.slash(
    name="hello",
    description="test",
    guild_ids=[965529769942855710]
)
async def hello(ctx:SlashContext):
    await ctx.send("World!")


client.run('OTcyNzY2ODU4MTcwMjE2NDY4.Ynd1vA.WHp29HMOj6JADKKgY3cTGkWBOtY') # run the bot with the token