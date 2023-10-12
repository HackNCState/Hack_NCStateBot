import datetime
import discord
from discord.ext import commands

from src.modules import Events

async def run(token):
  intents = discord.Intents.default()
  intents.members = True

  bot = commands.Bot(command_prefix='&', intents=intents)


  bot.invites = {}
  bot.code2role = {
      "y9JzshSpQr": 'Judge',
      "FEwQXxp7EG": 'Volunteer',
      "vrYaFPRYUs": 'Mentor',
      "CAA9DrJhgs": 'Sponsor'
  }

  def find_invite_by_code(invites, code):
    # Filter the invite list by the code
    result = list(filter(lambda x: x.code == code, invites))
    # Return the invite that was found
    return result[0] if len(result) == 1 else None
  bot.find_invite_by_code = find_invite_by_code

  def log(message, filepath="log.txt"):
          # Gather time and create formatted string from it
          now = datetime.datetime.now()
          date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
          # Open the log file and append the message with timestamp to end
          with open(filepath, 'a+') as f:
              f.write("%s:\t%s\n" % (date_time, message))
  bot.log = log

  await bot.add_cog(Events(bot))
  # ... Commands(bot) ...

  await bot.start(token)