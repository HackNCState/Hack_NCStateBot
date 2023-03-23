import dotenv
import os
from src import client
from src import life_support

# Load API keys from environment variables
dotenv.load_dotenv()
bot = client.Client()
life_support.keep_alive()
bot.run(os.getenv('TOKEN'))