import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, datetime, random, logging, requests
import json, yaml

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

config = yaml.safe_load(open("modules\\DirectMessagesConfig.yml", 'r', encoding="utf-8"))

class DirectMessages(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f'{time} DirectMessages module ready!')
        pass

def setup(bot):
    bot.add_cog(DirectMessages(bot))