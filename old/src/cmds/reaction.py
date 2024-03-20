import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Reaction(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} Reaction load!')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
        guild = self.bot.get_guild(payload.guild_id)
        # 判斷反應貼圖給予相對應身分組
        if payload.message_id == 1114422293024751749:
            if str(payload.emoji) == "✅":
                role = guild.get_role(969627339107479582)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "📢":
                role = guild.get_role(1114418672358924320)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "💬":
                role = guild.get_role(1114418672358924320)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "❤️":
                role = guild.get_role(1046732884628733952)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "🔕":
                role = guild.get_role(1114417888581918781)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "🎶":  # \U0001F3B6
                role = guild.get_role(1114418404615528468)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "♂️":
                role = guild.get_role(1025069054492426305)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "♀️":
                role = guild.get_role(974553210075381760)
                await payload.member.add_roles(role)
                await payload.member.send(f'你取得了 {role} 身分組!')
                print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
        else:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
        guild = self.bot.get_guild(payload.guild_id)
        # 判斷反應貼圖給予相對應身分組
        if payload.message_id == 1114422293024751749:
            if str(payload.emoji) == "✅":
                role = guild.get_role(969627339107479582)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "📢":
                role = guild.get_role(1114418672358924320)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "💬":
                role = guild.get_role(1114418672358924320)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "❤️":
                role = guild.get_role(1046732884628733952)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "🔕":
                role = guild.get_role(1114417888581918781)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "🎶":  # \U0001F3B6
                role = guild.get_role(1114418404615528468)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "♂️":
                role = guild.get_role(1025069054492426305)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
            if str(payload.emoji) == "♀️":
                role = guild.get_role(974553210075381760)
                user = guild.get_member(payload.user_id)
                await user.remove_roles(role)
                await user.send(f'你移除了 {role} 身分組')
                print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
        else:
            pass

def setup(bot):
    bot.add_cog(Reaction(bot))