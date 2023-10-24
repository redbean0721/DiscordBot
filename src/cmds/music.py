import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import pytube as pt

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Music(Cog_Extension):
    def __init__(self, bot):
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
        print(f'{time} Music ready!')
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.current_song = None

        # [[song, channel]]
        self.music_queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     #searching the item on youtube
    def search_yt(self, item):
        try:
            video = pt.Search(item).results[0]
            return {'source': video.streams.get_audio_only().url, 'title': video.title}
        except Exception:
            print('搜索 youtube 時發生異常')
            return False

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.current_song = self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            self.current_song = None

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.current_song = self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(help="搜尋YouTube影片")
    async def search(self, ctx, search):
        response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + search + '&key=' + data['yt_api_key'] + '&type=video&maxResults=1')
        jdata = response.json()
        url = "https://www.youtube.com/watch?v=" + jdata['items'][0]['id']['videoId']
        await ctx.send(url)

    @commands.command(help="撥放音樂(url/搜尋關鍵字)")
    async def play(self, ctx, *args):
        await ctx.reply("音樂功能暫停使用")
    #     # print(self.is_playing, self.is_paused)
    #     print('play command')
    #     query = " ".join(args)
        
    #     if ctx.author.voice is None:
    #         #you need to be connected so that the bot knows where to go
    #         await ctx.send("你先加入語音頻道!")
    #     elif self.is_paused:
    #         self.vc.resume()
    #     else:
    #         song = self.search_yt(query)
    #         title = "title"  # use this to access the title of the song
    #         if type(song) == type(True):
    #             await ctx.send("無法下載歌曲, 格式不正確請嘗試其他關鍵字, 這可能是由於播放列表或直播格式所致")
    #         else:
    #             await ctx.send(f'已將 **{song[title]}** 加入對列中')
    #             self.music_queue.append([song, ctx.author.voice.channel])
                
    #             if self.is_playing == False:
    #                 await self.play_music(ctx)

    # @commands.command(help="將歌曲添加到隊列的最前面")
    # async def priority_play(self, ctx, *args):
    #     print('priority_play command')
    #     query = " ".join(args)
        
    #     if ctx.author.voice is None:
    #         #you need to be connected so that the bot knows where to go
    #         await ctx.send("你先加入語音頻道!")
    #     elif self.is_paused:
    #         self.vc.resume()
    #     else:
    #         if ctx.author.guild_permissions.administrator == False:
    #             await ctx.send("你沒有權限!")
    #             return
    #         else:
    #             await ctx.send("Hello, admin")
    #         song = self.search_yt(query)
    #         title = "title"  # use this to access the title of the song
    #         if type(song) == type(True):
    #             await ctx.send("無法下載歌曲, 格式不正確請嘗試其他關鍵字, 這可能是由於播放列表或直播格式所致")
    #         else:
    #             await ctx.send(f'已將 **{song[title]}** 加入對列中')
    #             self.music_queue.insert(0, [song, ctx.author.voice.channel])
    #             if self.is_playing == False:
    #                 await self.play_music(ctx)

    # @commands.command(help="顯示當前正在播放的歌曲")
    # async def current(self, ctx):
    #     print('current command')
    #     if self.is_playing:
    #         # debugging
    #         if self.current_song is None:
    #             print('ERROR, 當前歌曲沒有, 但正在播放')
    #             return
    #         await ctx.send(f'正在播放: {self.current_song[0]["title"]}')
    #     else:
    #         await ctx.send("目前沒有正在播放的歌曲")

    # @commands.command(help="暫停播放")
    # async def pause(self, ctx, *args):
    #     print('pause command')
    #     if self.is_playing:
    #         await ctx.send("Pausing playback")
    #         self.is_playing = False
    #         self.is_paused = True
    #         self.vc.pause()

    # @commands.command(help="恢復播放")
    # async def resume(self, ctx, *args):
    #     print('resume command')
    #     if self.is_paused:
    #         await ctx.send("Resuming playback")
    #         self.is_paused = False
    #         self.is_playing = True
    #         self.vc.resume()

    # @commands.command(help="跳過當前歌曲")
    # async def skip(self, ctx):
    #     print('skip command')
    #     if self.vc != None and self.vc:
    #         await ctx.send("Skipping song")
    #         self.vc.stop()
    #         # try to play next in queue if it exists
    #         await self.play_music(ctx)

    # @commands.command(help="查看對列")
    # async def queue(self, ctx):
    #     print('queue command')
    #     retval = "接著撥放: ("
    #     if len(self.music_queue) < 10:
    #         retval += f'{len(self.music_queue)}/'
    #     else:
    #         retval += '10/'
    #     retval += f'{len(self.music_queue)})\n'
    #     for i in range(0, len(self.music_queue)):
    #         # display first 10 songs in the queue
    #         if i >= 10: 
    #             break
    #         retval += self.music_queue[i][0]['title'] + "\n"

    #     if retval:
    #         await ctx.send(f'正在播放:\n{self.current_song[0]["title"]}\n\n{retval}')
    #         # await ctx.send(retval)
    #     else:
    #         await ctx.send("對列是空的")

    # @commands.command(help="清除對列所有歌曲")
    # async def quere_c(self, ctx):
    #     print('clear command')
    #     if self.vc != None and self.is_playing:
    #         self.vc.stop()
    #     self.music_queue = []
    #     self.current_song = None
    #     await ctx.send("Music queue cleared")

    # @commands.command(help="讓我離開語音頻道")
    # async def leave(self, ctx):
    #     print('leave command')
    #     self.is_playing = False
    #     self.is_paused = False
    #     self.music_queue = []
    #     self.current_song = None
    #     await ctx.send(f'{ctx.message.author} 讓我離開語音頻道 :confused:')
    #     await self.vc.disconnect()

def setup(bot):
    bot.add_cog(Music(bot))




# 內容參考自 https://github.com/KingTingTheGreat/DiscordBot 的 music_cog.py