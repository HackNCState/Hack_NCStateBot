import discord
from discord.ext import commands
import datetime


class Client(discord.Client):

  def __init__(
    self,
    *args,
    **kwargs,
  ):
    # Initialize intents for the bot
    intents = discord.Intents.default()
    intents.members = True
    # Initialize discord client with arguments
    super().__init__(intents=intents, *args, **kwargs)
    # Initialize a dictionary to map servers to their available invites
    self.__invites = {}
    # Initialize bot variable and code to role map
    self.__bot = commands.Bot(command_prefix='&', intents=intents)
    self.__code2role = {
      "y9JzshSpQr": 'Judge',
      "FEwQXxp7EG": 'Volunteer',
      "vrYaFPRYUs": 'Mentor',
      "CAA9DrJhgs": 'Sponsor'
    }

  async def on_ready(self):
    # Loop through all servers the bot exists on
    for server in self.__bot.guilds:
      # Gather the invite links for these servers
      self.__invites[server.id] = await server.invites()
    log("Bot Activated")

  async def on_member_join(self, member):
    # Get the invite list for this user's server before the join
    original_invites = self.__invites[member.guild.id]
    # Get the invite list for after this user joined the server
    updated_invites = await member.guild.invites()
    for invite in original_invites:
      # Find the invite from our list of invites
      found_invite = find_invite_by_code(updated_invites, invite.code)
      # If the uses have updated, we found the code this user joined with
      if found_invite is not None and invite.uses < found_invite.uses:
        log(f"Member {member.name} Joined")
        log(f"Invite Code: {invite.code}")
        if invite.code in self.__code2role:
          try:
            role_name = self.__code2role.get(str(invite.code))
            await member.add_roles(
              discord.utils.get(member.guild.roles, name=role_name))
          except Exception as e:
            log(f"Error add role to {member.name}.")

  async def on_member_remove(self, member):
    # Update the invite list if a user leaves
    self.__invites[member.guild.id] = await member.guild.invites()


def find_invite_by_code(invites, code):
  # Filter the invite list by the code
  result = list(filter(lambda x: x.code == code, invites))
  # Return the invite that was found
  return result[0] if len(result) == 1 else None


def log(message, filepath="log.txt"):
  # Gather time and create formatted string from it
  now = datetime.datetime.now()
  date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  # Open the log file and append the message with timestamp to end
  with open(filepath, 'a+') as f:
    f.write("%s:\t%s\n" % (date_time, message))
