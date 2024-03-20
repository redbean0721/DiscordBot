import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import secrets

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Admin(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} Admin load!')

    #kick command
    @commands.command(help="踢出成員")
    @commands.has_permissions(manage_messages = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.send(f"已踢出成員 {member.mention}, 原因: {reason}")

    #ban command
    @commands.command(help="封鎖成員")
    @commands.has_permissions(manage_messages = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f"已封鎖成員 {member.mention}, 原因: {reason}")

    #unban command
    @commands.command(help="解除封鎖成員")
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, user : discord.User):
        guild = ctx.guild
        bans = await ctx.guild.bans()
        for i in bans:
            if(user in i):  
                await guild.unban(user=user)
                await ctx.send(f'已解除封鎖成員 {user.mention}')


def setup(bot):
    bot.add_cog(Admin(bot))