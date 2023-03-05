import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests, sys
import json, yaml

log_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
logging.basicConfig(filename=f'log/{log_time}.log', level=logging.INFO, format='[%(asctime)s %(levelname)s]: %(message)s')

with open('setting.json', mode='r',encoding='utf8') as setting:
    data = json.load(setting)

with open('version.json', mode='r',encoding='utf8') as v:
    version = json.load(v)

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=(str(data['prefix'])), intents=intents)

@bot.event
async def on_ready():
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} >> Bot is online <<\n{time} 目前登入身份:', bot.user)
    await bot.change_presence(status=discord.Status(data['bot_status']), activity=discord.Game(data['bot_activity']))
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} 正在同步斜線命令...')
    await asyncio.sleep(2) #單位: 秒
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} 斜線命令同步完成\n{time} >> Bot is Ready <<\n{time} 目前版本為:', version['version'])

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
async def close(ctx):
    if ctx.author.id == int(data['owner_id']):
        await ctx.send("Closeing bot...")
        await asyncio.sleep(1)
        await bot.close()
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

@bot.command()
async def restart(ctx):
    if ctx.author.id == int(data['owner_id']):
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

# cmds
@bot.command()
async def load(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} Loading {extension} ...')
        bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

@bot.command()
async def unload(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} Un - Loading {extension} ...')
        bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Un - Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

@bot.command()
async def reload(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} RE - Loading {extension} ...')
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'RE - Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

# modules
@bot.command()
async def load_mod(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} Loading {extension} ...')
        bot.load_extension(f'modules.{extension}')
        await ctx.send(f'Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

@bot.command()
async def unload_mod(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} Un - Loading {extension} ...')
        bot.unload_extension(f'modules.{extension}')
        await ctx.send(f'Un - Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

@bot.command()
async def reload_mod(ctx, extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    if ctx.author.id == int(data['owner_id']):
        print(f'{time} RE - Loading {extension} ...')
        bot.reload_extension(f'modules.{extension}')
        await ctx.send(f'RE - Loaded {extension} done.')
    else:
        await ctx.send(f"{ctx.author.mention} 你沒有權限")

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

for filename in os.listdir('./modules'):
	if filename.endswith('.py'):
		bot.load_extension(f'modules.{filename[:-3]}')

if __name__ == '__main__': 
    bot.run(os.getenv('TOKEN'))