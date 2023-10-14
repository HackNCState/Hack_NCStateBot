import discord
from discord.ext import commands

from src import HackathonClient

class Events(commands.Cog):
    def __init__(self, bot: HackathonClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("Bot Activated")
        for server in self.bot.guilds:
            # Gather the invite links for these servers
            self.bot.invites[server.id] = await server.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get the invite list for this user's server before the join
        original_invites = self.bot.invites[member.guild.id]
        # Get the invite list for after this user joined the server
        updated_invites = await member.guild.invites()
        for invite in original_invites:
            # Find the invite from our list of invites
            found_invite = self.bot.find_invite_by_code(updated_invites, invite.code)
            # If the uses have updated, we found the code this user joined with
            if found_invite is not None and invite.uses < found_invite.uses:
                self.bot.log(f"Member {member.name} Joined")
                self.bot.log(f"Invite Code: {invite.code}")
                if invite.code in self.bot.code2role:
                    try:
                        role_name = self.bot.code2role.get(str(invite.code))
                        await member.add_roles(discord.utils.get(member.guild.roles, name=role_name))
                    except Exception as e:
                        self.bot.log(f"Error add role to {member.name}.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Update the invite list if a user leaves
        self.bot.invites[member.guild.id] = await member.guild.invites()
