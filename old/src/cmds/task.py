import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

with open('cmds/task/task.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
        print(f'{time} Task load!')
        self.counter = 0

        # async def interval():
        #     await self.bot.wait_until_ready()
        #     with open('cmds/task.json', 'r', encoding='utf8') as tfile:
        #             tdata = json.load(tfile)
        #             self.channel = self.bot.get_channel(int(tdata['interval_channel']))
        #             while not self.bot.is_closed():
        #                 await self.channel.send(str(tdata['interval_text']))
        #                 await asyncio.sleep(int(tdata['interval_time']))

        # self.bg_task = self.bot.loop.create_task(interval())
    
        # async def time_task():
        #     await self.bot.wait_until_ready()
        #     with open('cmds/task.json', 'r', encoding='utf8') as tfile:
        #             tdata = json.load(tfile)
        #             self.channel = self.bot.get_channel(int(tdata['time_task_channel']))
        #             while not self.bot.is_closed():
        #                 now_time = datetime.datetime.now().strftime('%H:%M')
        #                 if now_time == tdata['time_task_time'] and self.counter ==0:
        #                     await self.channel.send(str(tdata['time_task_text']))
        #                     self.counter = 1
        #                     await asyncio.sleep(1)
        #                 else:
        #                     await asyncio.sleep(1)
        #                     pass

        # self.bg_task = self.bot.loop.create_task(time_task())

    @commands.command()
    async def set_interval(self, ctx, interval_channel: int, interval_text, interval_time):
        with open('cmds/task.json', 'r', encoding='utf8') as tfile:
            tdata = json.load(tfile)
        tdata['interval_channel'] = int(interval_channel)
        tdata['interval_text'] = str(interval_text)
        tdata['interval_time'] = int(interval_time)
        with open('cmds/task.json', 'w', encoding='utf8') as tfile:
            json.dump(tdata, tfile, indent=4)
        await ctx.send(f'Set Interval:\nChannel: {int(interval_channel)}\nText: {str(interval_text)}\nTime: {int(interval_time)} s')

        # self.channel = self.bot.get_channel(channel_id)
        # await ctx.send(f'Set Channel: {self.channel.mention}')

    @commands.command()
    async def set_time(self, ctx, time):
        self.counter = 0
        with open('cmds/task.json', 'r', encoding='utf8') as tfile:
            tdata = json.load(tfile)
        tdata['time'] = time
        with open('cmds/task.json', 'w', encoding='utf8') as tfile:
            json.dump(tdata, tfile, indent=4)
        await ctx.send(f'Set Time: {time}')

    # @commands.slash_command(name="set_interval_channel", description="Set Interval channel")
    # async def set_channel(self, ctx, channel_id):
    #     self.channel = self.bot.get_channel(int(channel_id))
    #     await ctx.respond(f'Set Channel: {self.channel.mention}')
    
    # @commands.slash_command(name="set_time", description="Set Task time")
    # async def set_time(self, ctx, time):
    #     self.counter = 0
    #     with open('cmds/task.json', 'r', encoding='utf8') as tfile:
    #         tdata = json.load(tfile)
    #     tdata['time'] = time
    #     with open('cmds/task.json', 'w', encoding='utf8') as tfile:
    #         json.dump(tdata, tfile, indent=4)
    #     await ctx.respond(f'Set Time: {time}')

def setup(bot):
    bot.add_cog(Task(bot))