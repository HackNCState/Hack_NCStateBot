import datetime
import os
import discord
from discord.ext import commands

# Named the bot class HackathonClient instead of Client to avoid confusion with discord.Client
# which is a superclass.
class HackathonClient(commands.Bot):    
    code2role = {
        os.getenv("INVITE_JUDGE"): 1168256795106611205,
        os.getenv("INVITE_VOLUNTEER"): 1168256795106611203,
        os.getenv("INVITE_MENTOR"): 1168256795106611204,
        os.getenv("INVITE_SPONSOR"): 1168256795106611206,
    }

    def __init__(
            self, 
            command_prefix: str = "&", 
            intents: discord.Intents = discord.Intents.default(),  
            cogs: list[type[commands.Cog]] = []
    ):
        self.invites = {}
        self.setup_cogs = cogs

        super().__init__(command_prefix, intents=intents)


    async def setup_hook(self) -> None:
        for cog in self.setup_cogs:
            await self.add_cog(cog(self))
        return await super().setup_hook()

    @staticmethod 
    def find_invite_by_code(invites, code):
        # Filter the invite list by the code
        result = list(filter(lambda x: x.code == code, invites))
        # Return the invite that was found
        return result[0] if len(result) == 1 else None
    
    @staticmethod
    def log(message, filepath="log.txt"):
        # Gather time and create formatted string from it
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        # Open the log file and append the message with timestamp to end
        with open(filepath, 'a+') as f:
            f.write("%s:\t%s\n" % (date_time, message))
