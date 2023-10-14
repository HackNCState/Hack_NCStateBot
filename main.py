import discord
import dotenv
import os
from discord.ext import commands

from src import client
from src import life_support
from src.cogs import Events

# Load API keys from environment variables
dotenv.load_dotenv()

# keep-alive
life_support.keep_alive()

# Create the bot
token = os.getenv("TOKEN")
if token is not None:
    intents = discord.Intents.default()
    intents.members = True

    cogs: list[type[commands.Cog]] = [
        Events,
    ]

    bot = client.HackathonClient(cogs=cogs, intents=intents)
    bot.run(token)