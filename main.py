import dotenv
import os
from src import client
from src import life_support

# Load API keys from environment variables
dotenv.load_dotenv()

# keep-alive
life_support.keep_alive()

# Create the bot
bot = client.HackathonClient()
bot.run(os.getenv("TOKEN"))