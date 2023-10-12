import asyncio
import dotenv
import os
from src import client
from src import life_support

# Load API keys from environment variables
dotenv.load_dotenv()
life_support.keep_alive()
asyncio.run(client.run(os.getenv('TOKEN')))