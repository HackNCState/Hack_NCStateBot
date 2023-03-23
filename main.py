import dotenv
import os
from src import client

# Load API keys from environment variables
dotenv.load_dotenv()
bot = client.Client()
bot.run(os.getenv('TOKEN'))