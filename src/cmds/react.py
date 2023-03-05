import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class React(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} React load!')

    @commands.command()
    async def pic(self, ctx):
        random_pic = random.choice(data['pic'])
        pic = discord.File(random_pic)
        await  ctx.send(file= pic)

    @commands.command()
    async def web(self, ctx):
        random_pic = random.choice(data['url_pic'])
        await ctx.send(random_pic)

def setup(bot):
    bot.add_cog(React(bot))