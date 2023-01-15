import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

with open('cmds/join_guilds.json', mode='r', encoding='utf8') as f:
    guilds_dict = json.load(f)

with open('cmds/reaction.json', mode='r', encoding='utf8') as a:
    reaction = json.load(a)

class Event(Cog_Extension):
    print(f'{time} Event load!')

    """取得Json API 資料"""

    @commands.command()
    async def test(self, ctx):
        response = requests.get('http://127.0.0.1:3000/posts/1')

        # 取得原來資料
        data = response.json()

        # 新增一筆資料到原來資料裡
        data['new'] = "This is a new data"

        updata = requests.put('http://127.0.0.1:3000/posts/1', json = data)
        await ctx.send(updata)

    """"""

##

    """偵測文字-自動聊天"""

    @commands.Cog.listener()
    async def on_message(self, msg):
        egg = ['誰叫我', '我在這~', '怎麼了 <:ha:1047493102170021898>', 'none', 'none', 'none']
        random_choice_egg = random.choice(egg)
        if 'ㄒㄧㄠˊ 蛋蛋' in  msg.content and msg.author != self.bot.user and random_choice_egg != 'none':
            await msg.channel.send(random_choice_egg)

        good_morning = ['安', '安安', 'none', 'none']
        random_choice_good_morning = random.choice(good_morning)
        if '安安' in  msg.content and msg.author != self.bot.user and random_choice_good_morning != 'none':
            await msg.channel.send(random_choice_good_morning)

        # emo = ['...', 'none', 'none', 'none', 'none']
        # random_choice_emo = random.choice(emo)
        # if '...' in  msg.content and msg.author != self.bot.user and random_choice_emo != 'none':
        #     await msg.channel.send(random_choice_emo)

    """"""

##

    """使用貼圖反映身分組"""

        # if payload.message_id == 1060240402248122459:
        #     guild = self.bot.get_guild(payload.guild_id) # 取得當前所在伺服器
        #     role = guild.get_role(1058049761682403348) #取得伺服器內指定的身分組
        #     await payload.member.add_roles(role) # 給予該成員身分組
        #     await payload.member.send(f'你取得了 {role} 身分組!')
        #     print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
        # else:
        #     pass

###爛學校討論群🎄 🦌 🛷 🦌🎄
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # 判斷反應貼圖給予相對應身分組
        if payload.message_id == 1060240402248122459:
            guild = self.bot.get_guild(payload.guild_id) # 取得當前所在伺服器
            role = guild.get_role(1058049761682403348) #取得伺服器內指定的身分組
            await payload.member.add_roles(role) # 給予該成員身分組
            await payload.member.send(f'你取得了 {role} 身分組!')
            print(f'{time} Add {role} to {payload.member}, {payload.emoji} in {guild}')
        else:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # 判斷反應貼圖移除相對應身分組
        if payload.message_id == 1060240402248122459:
            guild = self.bot.get_guild(payload.guild_id) # 取得當前所在伺服器
            user = guild.get_member(payload.user_id) # 取得使用者
            role = guild.get_role(1058049761682403348) #取得伺服器內指定的身分組
            await user.remove_roles(role) # 移除該成員身分組
            await user.send(f'你移除了 {role} 身分組!')
            print(f'{time} Remove {role} to {payload.member}, {payload.emoji} in {guild}')
        else:
            pass

    """"""

##

    """各伺服器成員加入"""

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = guilds_dict[member.guild.id]
        await self.bot.get_channel(int(channel_id)).send(f'歡迎 {member.mention} 加入伺服器!🎉')

    @commands.command(help='設定歡迎訊息的發送頻道')
    @commands.has_permissions(manage_messages = True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        guilds_dict[ctx.guild.id] = channel.id
        with open('cmds/join_guilds.json', mode='w', encoding='utf8') as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
        await ctx.send(f'將 "{ctx.message.guild.name}" 的歡迎訊息發送到 "{channel.name}"')

    # Optional:
    # So if your bot leaves a guild, the guild is removed from the dict
    # 如果你的機器人離開了伺服器，這個伺服器就會從字典中刪除
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds_dict.pop(guild.id)
        with open('cmds/join_guilds.json', mode='w', encoding='utf8') as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
            
    """"""

##

    """審核日誌"""



    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        channel = self.bot.get_channel(1058926594997112922)
        counter = 1
        async for entry in msg.guild.audit_logs(action=discord.AuditLogAction.message_delete):
            if counter ==1:
                # await channel.send(entry.user.name)
                print(f'{time} "{entry.user}" 刪除了 "{msg.guild}" 伺服器 "{str(msg.author)}" 的訊息, 內容: "{str(msg.content)}"')
                await channel.send(f'{time} "{entry.user}" 刪除了 "{msg.guild}" 伺服器 "{str(msg.author)}" 的訊息, 內容: "{str(msg.content)}"')
                counter += 1

    """"""

##

    """"""

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, command_error):
    #     #檢查指令是否有自己的error handler：如果有就略過
    #     if hasattr(ctx.command, 'on_error'):
    #        return
    #     if isinstance(command_error, commands.errors.MissingRequiredArgument):
    #         await ctx.send(f'缺少必要的參數: {command_error}')
    #     elif isinstance(command_error, commands.errors.CommandNotFound):
    #         await ctx.send("指令未找到")
    #     else:
    #        await ctx.send(f'發生錯誤: {command_error}')

    """"""

def setup(bot):
    bot.add_cog(Event(bot))



    # @commands.Cog.listener()
    # async def on_message(self, msg):
    #     if 'kg鞍' in  msg.content and msg.author != self.bot.user:
    #         kg鞍 = ['誰叫我', '我在這~', '怎麼了', 'none', 'none', 'none']
    #         random_choice_kg鞍 = random.choice(kg鞍)
    #         if random_choice_kg鞍 != 'none':
    #             await msg.channel.send(random_choice_kg鞍)
    
    # @commands.Cog.listener()
    # async def on_message(self, msg):
    #     if '臭蛋蛋' in msg.content and msg.author != self.bot.user:
    #         await msg.channel.send(f'<@1017630139019968643>')

    # @commands.Cog.listener()
    # async def on_message(self, msg):
    #    if 'kg鞍' in  msg.content and msg.author != self.bot.user:
    #        kg鞍 = ['誰叫我', '我在這~', '怎麼了', '']
    #        await msg.channel.send(random.choice(kg鞍))
    #    if '...' in  msg.content and msg.author != self.bot.user:
    #        emo = ['......', '']
    #        await msg.channel.send(random.choice(emo))

#-----

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     print(f'{member} join!')
    #     channel = self.bot.get_channel(int(1057647364749393970))
    #     await channel.send(f'歡迎 {member.name} 加入伺服器!')

    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     print(f'{member} leave!')
    #     channel = self.bot.get_channel(int(1057647364749393970))
    #     await channel.send(f'{member.name} 離開了伺服器qq')

#------

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, command_error):
    #     #檢查指令是否有自己的error handler：如果有就略過
    #     if hasattr(ctx.command, 'on_error'):
    #        return
    #     if isinstance(command_error, commands.errors.MissingRequiredArgument):
    #         await ctx.send(f'缺少必要的參數: {command_error}')
    #     elif isinstance(command_error, commands.errors.CommandNotFound):
    #         await ctx.send("指令未找到")
    #     else:
    #        await ctx.send(f'發生錯誤: {command_error}')