import discord
from discord.ext import commands
from discord import app_commands

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="test", description="測試指令")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is a test command.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Test(bot))