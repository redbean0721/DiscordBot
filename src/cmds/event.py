import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

with open('cmds/join_guilds.json', mode='r', encoding='utf8') as guild:
    guilds_dict = json.load(guild)

with open('cmds/reaction.json', mode='r', encoding='utf8') as a:
    reaction = json.load(a)

class Event(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} Event load!')

    # """取得Json API 資料"""

    # @commands.command()
    # async def test(self, ctx):
    #     response = requests.get('http://127.0.0.1:3000/posts/1')

    #     # 取得原來資料
    #     data = response.json()

    #     # 新增一筆資料到原來資料裡
    #     data['new'] = "This is a new data"

    #     updata = requests.put('http://127.0.0.1:3000/posts/1', json = data)
    #     await ctx.send(updata)

    # """"""

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
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
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
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
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
        folder = f'cmds/guild'
        guild_folder = f'{folder}/{member.guild.id}'
        on_member = f'{guild_folder}/on_member.json'
        if not os.path.exists(guild_folder):
            # os.makedirs(guild_folder)
            pass
        pass
        if os.path.isfile(f'{on_member}'):
            with open(f'{on_member}', mode='r', encoding='utf8') as filt:
                odata = json.load(filt)
                channel_id = odata['welcome_channel']
                await self.bot.get_channel(int(channel_id)).send(f'歡迎 {member.mention} 加入伺服器!🎉')
        elif not os.path.isfile(f'{on_member}'):
            pass
        else:
            print("on_member 發生錯誤")

    @commands.command(help="設定歡迎訊息的發送頻道")
    @commands.has_permissions(manage_messages = True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        folder = f'cmds/guild'
        guild_folder = f'{folder}/{ctx.guild.id}'
        on_member = f'{guild_folder}/on_member.json'
        if not os.path.exists(guild_folder):
            os.makedirs(guild_folder)
        if not os.path.isfile(f'{on_member}'):
            with open (f'{on_member}', mode="a+", encoding="utf8") as filt:
                odata = {"welcome_channel":f'{channel.id}'}
                json.dump(odata, filt, indent=4, ensure_ascii=False)
            await ctx.send(f'將 "{ctx.message.guild.name}" 的歡迎訊息發送到 {channel.mention}')
        elif os.path.isfile(f'{on_member}'):
            with open(f'{on_member}', mode='r', encoding='utf8') as filt:
                gg = json.load(filt)
            gg['welcome_channel'] = f'{channel.id}'
            with open(f'{on_member}', mode="w", encoding="utf8") as filt:
                json.dump(gg, filt, indent=4, ensure_ascii=False)
            await ctx.send(f'將 "{ctx.message.guild.name}" 的歡迎訊息更改為 {channel.mention}')
        else:
            print("set_welcome_channel 發生錯誤")


    # @commands.command(help='設定歡迎訊息的發送頻道')
    # @commands.has_permissions(manage_messages = True)
    # async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
    #     guilds_dict[ctx.guild.id] = channel.id
    #     with open('cmds/join_guilds.json', mode='w', encoding='utf8') as f:
    #         json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    #     await ctx.send(f'將 "{ctx.message.guild.name}" 的歡迎訊息發送到 "{channel.name}"')


    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     print(f'{member} leave!')
    #     channel = self.bot.get_channel(int(1057647364749393970))
    #     await channel.send(f'{member.name} 離開了伺服器qq')

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
        channel = self.bot.get_channel(int(data['delete_message_channel']))
        counter = 1
        async for entry in msg.guild.audit_logs(action=discord.AuditLogAction.message_delete):
            if counter ==1:
                # await channel.send(entry.user.name)
                time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
                print(f'{time} "{entry.user}" 刪除了 "{msg.guild}" 伺服器 "{msg.channel}" 頻道 "{str(msg.author)}" 的訊息, 內容: "{str(msg.content)}"')
                await channel.send(f'{time} "{entry.user}" 刪除了 "{msg.guild}" 伺服器 "{msg.channel}" 頻道 "{str(msg.author)}" 的訊息, 內容: "{str(msg.content)}"')
                counter += 1

    """"""

def setup(bot):
    bot.add_cog(Event(bot))