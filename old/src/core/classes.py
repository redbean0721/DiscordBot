import discord
from discord.ext import commands

class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class Cog_Modules(commands.Cog):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.status = 0