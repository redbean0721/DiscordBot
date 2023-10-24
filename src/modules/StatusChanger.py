import discord
from discord.ext import commands
from discord.ext import tasks
from core.classes import Cog_Extension
from core.classes import Cog_Modules
import asyncio, os, datetime, random, logging, requests
import json, yaml

config = yaml.safe_load(open("modules\\StatusChangerConfig.yml", 'r', encoding="utf-8"))

interval = config.get("Change-Interval")

# class StatusUpdater(Cog_Extension):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
#         print(f'{time} StatusChanger module ready!')
#         self.status = 0

class StatusUpdater(Cog_Modules):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} StatusChanger module ready!')

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.update_status.is_running():
            self.update_status.start()

    @tasks.loop(seconds=interval)
    async def update_status(self):
        self.status += 1
        if self.status == len(config.get("Status-list")):
            self.status = 0

        message = config.get("Status-list")[self.status]
        server_count = len(self.bot.guilds)
        status_message = message.format(server_count=server_count)

        await self.bot.change_presence(activity=discord.Game(name=status_message, type=3))

    @update_status.before_loop
    async def before_update_status(self):
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
        """Wait for bot to fully start before updating status"""
        await self.bot.wait_until_ready()
        print(f'{time} Launching status updater!')

def setup(bot):
    bot.add_cog(StatusUpdater(bot))