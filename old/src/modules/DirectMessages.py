import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, datetime, random, logging, requests
import json, yaml

config = yaml.safe_load(open("modules\\DirectMessagesConfig.yml", 'r', encoding="utf-8"))

class DirectMessages(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} DirectMessages module ready!')
    pass

def setup(bot):
    bot.add_cog(DirectMessages(bot))