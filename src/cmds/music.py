import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
# load our local env so we dont have the token in public
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

with open('setting.jsonc', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Music(Cog_Extension):
    print(f'{time} Music load!')

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
    @commands.command(help="加入你所在的語音頻道")
    async def join(self, ctx,):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.reply(f'加入了 `{ctx.author}` 的語音頻道')

    @commands.command(help="讓我離開語音頻道")
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        try:
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                await voice_client.disconnect()
                await ctx.reply(f'{ctx.message.author} 讓我離開語音頻道 :confused:')
                print("Bot Command: leave from User {}".format(ctx.message.author))
            else:
                await ctx.send("Error could not leave voice channel")
                await ctx.reply(e)
        except Exception as e:
            # print("Error could not leave voice channel")
            await ctx.reply("機器人沒有在語音頻道 :face_with_raised_eyebrow: ")
            # print(e)

# command to play sound from a youtube URL
    @commands.command(help="撥放音樂(url/搜尋關鍵字)")
    async def play(self, ctx, msg):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.reply("機器人正在撥放音樂 (對列系統還沒寫)")
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
                await ctx.reply('撥放中...')
        else:
            search = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + msg + '&key=' + data['yt_api_key'] + '&type=video&maxResults=1')
            jdata = search.json()
            url = "https://www.youtube.com/watch?v=" + jdata['items'][0]['id']['videoId']

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
                await ctx.reply('撥放中...')

    @commands.command(help="搜尋YouTube影片")
    async def search(self, ctx, search):
        response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + search + '&key=' + data['yt_api_key'] + '&type=video&maxResults=1')
        jdata = response.json()
        url = "https://www.youtube.com/watch?v=" + jdata['items'][0]['id']['videoId']
        await ctx.send(url)

# command to resume voice if it is paused
    @commands.command(help="恢復播放")
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.reply('播放已恢復')

    # command to pause voice if it is playing
    @commands.command(help="暫停播放")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.reply('播放已暫停')

    # command to stop voice
    @commands.command(help="停止播放")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.reply('停止撥放...')

def setup(bot):
    bot.add_cog(Music(bot))