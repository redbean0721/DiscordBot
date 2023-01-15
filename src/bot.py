import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
log_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
logging.basicConfig(filename=f'log/{log_time}.log', level=logging.INFO, format='[%(asctime)s %(levelname)s]: %(message)s')

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

bot = commands.Bot

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=(str(data['prefix'])), intents=intents)

@bot.event
async def on_ready():
    print(f'{time} >> Bot is online <<\n{time} 目前登入身份:', bot.user)
    await bot.change_presence(status=discord.Status(data['Bot-Status']), activity=discord.Game(data['Bot-Activity']))
    print(f'{time} 正在同步斜線命令...')
    await asyncio.sleep(3) #單位: 秒
    print(f'{time} 斜線命令同步完成\n{time} >> Bot is Ready <<')
    # print(f'{time} Done (3.978s)! For help, type "help"')


# """ 各伺服器成員加入頻道設定 """

# with open('guilds.json', mode='r', encoding='utf8') as f:
#     guilds_dict = json.load(f)

# @bot.event
# async def on_member_join(member):
#     channel_id = guilds_dict[member.guild.id]
#     await bot.get_channel(int(channel_id)).send(f'歡迎 {member.mention} 加入伺服器!🎉')


# @bot.command(help='設定歡迎訊息的發送頻道')
# async def set_welcome_channel(ctx, channel: discord.TextChannel):
#     guilds_dict[ctx.guild.id] = channel.id
#     with open('guilds.json', mode='w', encoding='utf-8') as f:
#         json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
#     await ctx.send(f'將 {ctx.message.guild.name} 的歡迎訊息發送到 {channel.name}')


# # Optional:
# # So if your bot leaves a guild, the guild is removed from the dict
# # 如果你的機器人離開了伺服器，這個伺服器就會從字典中刪除
# @bot.event
# async def on_guild_remove(guild):
#     guilds_dict.pop(guild.id)
#     with open('guilds.json', mode='w', encoding='utf-8') as f:
#         json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

# """"""

# @bot.event
# async def on_message(ctx):
#     print(f'[%H:%M:%S INFO]: [{ctx.guild}] <{ctx.author}>')

@bot.event
async def on_command_error(ctx, command_error):
    #檢查指令是否有自己的error handler：如果有就略過
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(command_error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'缺少必要的參數: {command_error}')
    elif isinstance(command_error, commands.errors.CommandNotFound):
        await ctx.send("指令未找到")
    else:
        await ctx.send(f'發生錯誤: {command_error}')

@bot.command()
async def load(ctx, extension):
    print(f'{time} Loading {extension} ...')
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
    print(f'{time} Un - Loading {extension} ...')
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
    print(f'{time} RE - Loading {extension} ...')
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'RE - Loaded {extension} done.')

modules = []
cmds = []

for filename in os.listdir('./modules'):
	if filename.endswith('.py'):
		bot.load_extension(f'modules.{filename[:-3]}')

for filename in os.listdir('./cmds'):
	if filename.endswith('.py'):
		bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == '__main__': 
    bot.run(str(data['TOKEN']))