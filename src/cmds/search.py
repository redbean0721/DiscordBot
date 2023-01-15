import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import secrets
# load our local env so we dont have the token in public
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Search(Cog_Extension):
    print(f'{time} Search load!')

    @commands.command(help="")
    async def play1(self, ctx, msg):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
        elif msg.startswith('http') and '://' in msg and self.bot:
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if not voice.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(msg, download=False)
                URL = info['url']
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()
                await ctx.send('撥放中...')
            # check if the bot is already playing
            # else:
            #     await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
            #     return
        else:
            search = requests.get(data['youtube_api_url'] + msg + '&key=' + data['youtube_api_key'] + '&type=video&maxResults=1')
            jdata = search.json()
            url = data['youtube_watch'] + jdata['items'][0]['id']['videoId']
            # await ctx.send(url)

            # use 'url' to play music
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if not voice.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['url']
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()
                await ctx.send('撥放中...')
            # check if the bot is already playing
            # else:
            #     await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
            #     return


    @commands.command(help="")
    async def search1(self, ctx, search):
        response = requests.get(data['youtube_api_url'] + search + '&key=' + data['youtube_api_key'] + '&type=video&maxResults=1')
        jdata = response.json()
        url = data['youtube_watch'] + jdata['items'][0]['id']['videoId']
        await ctx.send(url)


# # command to play sound from a youtube URL
#     @commands.command(help="播放音樂")
#     async def play(self, ctx, url):
#         YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#         voice = get(self.bot.voice_clients, guild=ctx.guild)
#         if not voice.is_playing():
#             with YoutubeDL(YDL_OPTIONS) as ydl:
#                 info = ydl.extract_info(url, download=False)
#             URL = info['url']
#             voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#             voice.is_playing()
#             await ctx.send('撥放中...')
# # check if the bot is already playing
#         else:
#             await ctx.send("機器人正在撥放音樂 ||對列系統還沒寫||")
#             return

    # https://www.googleapis.com/youtube/v3/search?part=snippet&q=搜尋的字串&key=API key&type=video&maxResults=影片的數量

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

def setup(bot):
    bot.add_cog(Search(bot))

# @commands.command(help="")
# async def test1(self, ctx, msg):
#     voice = get(self.bot.voice_clients, guild=ctx.guild)
#     if voice.is_playing():
#         await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
#     elif msg.startswith('http') and '://' in msg and self.bot:
#         YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#         voice = get(self.bot.voice_clients, guild=ctx.guild)
#         if not voice.is_playing():
#             with YoutubeDL(YDL_OPTIONS) as ydl:
#                 info = ydl.extract_info(msg, download=False)
#             URL = info['url']
#             voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#             voice.is_playing()
#             await ctx.send('撥放中...')
#         # check if the bot is already playing
#         # else:
#         #     await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
#         #     return
#     else:
#         search = requests.get(data['youtube_api_url'] + msg + '&key=' + data['youtube_api_key'] + '&type=video&maxResults=1')
#         jdata = search.json()
#         url = data['youtube_watch'] + jdata['items'][0]['id']['videoId']
#         # await ctx.send(url)

#         # use 'url' to play music
#         YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#         voice = get(self.bot.voice_clients, guild=ctx.guild)
#         if not voice.is_playing():
#             with YoutubeDL(YDL_OPTIONS) as ydl:
#                 info = ydl.extract_info(url, download=False)
#             URL = info['url']
#             voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#             voice.is_playing()
#             await ctx.send('撥放中...')
#         # check if the bot is already playing
#         # else:
#         #     await ctx.send("機器人正在撥放音樂 (對列系統還沒寫)")
#         #     return