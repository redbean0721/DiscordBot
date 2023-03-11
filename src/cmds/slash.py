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

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

with open('version.json', mode='r',encoding='utf8') as v:
    version = json.load(v)

class Slash(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} Slash load!')

    """Admin"""

    #kick command
    @commands.slash_command(description="踢出成員")
    @commands.has_permissions(manage_messages = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None ):
        await member.kick(reason = reason)
        await ctx.respond(f"{ctx.message.author.mention} 踢出成員 {member.mention}")

    #ban command
    @commands.slash_command(description="封鎖成員")
    @commands.has_permissions(manage_messages = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None ):
        await member.ban(reason = reason)
        await ctx.respond(f"{ctx.message.author.mention} 封鎖成員 {member.mention}")

    #unban command
    @commands.slash_command(description="解除封鎖成員")
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, user : discord.User):
        guild = ctx.guild
        bans = await ctx.guild.bans()
        for i in bans:
            if(user in i):  
                await guild.unban(user=user)
                await ctx.respond(f'{ctx.message.author.mention} 解除封鎖成員 {user}')

    """"""

##

    """Event"""

##

    """Fun"""

##

    """Main"""

    @commands.slash_command(description="跟你say Hellow")
    async def hi(self, ctx):
        await ctx.respond(random.choice(['誰叫我', '我在這~', '怎麼了', '?']))

    @commands.slash_command(description="ping我看我ㄉ延遲")
    async def ping(self, ctx):
        yt_api_url = 'https://www.googleapis.com/youtube/v3/search?key=' + data['yt_api_key']
        response_yt_api = requests.get(yt_api_url)
        if response_yt_api.status_code == 200:
            await ctx.send(f'Discord延遲 {round(self.bot.latency*1000)} ms\nYouTube API延遲 {round(response_yt_api.elapsed.total_seconds()*1000)} ms')
        else:
            await ctx.send(f"網路錯誤, 請稍後再試")
            
    @commands.slash_command(description="讓我幫你說話")
    async def say(self, ctx, msg):
        if msg != ("@everyone") and msg != ("@here"):
            await ctx.respond(f'訊息已傳送', ephemeral=True)
            async with ctx.typing():
                await asyncio.sleep(4)
            await ctx.send(msg)
        else:
            await ctx.respond(f'{msg.author.mention}你不可以@everyone或@here!!')

    @commands.slash_command(description="清除訊息")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.respond(f'{ctx.message.author.mention} 已刪除 {num} 則訊息')

    @commands.slash_command(description="隨機生成一串密碼")
    async def password(self, ctx, n_bytes: int = 18):
        if n_bytes not in range(3, 1401):
            return await ctx.respond("請輸入 3-1400 內的數字")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.respond(f"密碼已發送至您的私人訊息", ephemeral=True)
        await ctx.author.respond(f"🎁 **這是您的密碼:**\n```{secrets.token_urlsafe(n_bytes)}```")

    @commands.slash_command(description="關於我")
    async def info(self, ctx):
        embed=discord.Embed(title="關於我", description=f'{self.bot.user}', color=0x00fbff, timestamp= datetime.datetime.now())
        embed.add_field(name="開發者 Developers", value="redbean0721#5582", inline=False)
        embed.add_field(name="源碼 Source", value="https://github.com/redbean0721/DiscordBot", inline=False)
        embed.add_field(name="協助 Support Server", value="https://discord.gg/9hwuNYXA4q", inline=True)
        embed.add_field(name="版本 Version", value=(version['version']), inline=False)
        embed.add_field(name="使用語言", value="discord.py", inline=True)
        embed.add_field(name="指令 Prefix", value=(data['prefix']), inline=False)
        embed.add_field(name="服務中的伺服器 Server count", value=f"{len(self.bot.guilds)}", inline=False)
        embed.add_field(name="機器人延遲", value=f'{round(self.bot.latency*1000)} ms', inline=False)
        embed.add_field(name="API延遲", value=f'{round(self.bot.ws.latency*1000)} ms', inline=False)
        embed.set_footer(text="Made with ❤")
        await ctx.respond(embed=embed)

    """"""

##

    """Music""" # OK

    @commands.slash_command(description="加入你所在的語音頻道")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.respond("請先加入語音頻道")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.respond(f'加入了 `{ctx.author}` 的語音頻道')
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.slash_command(description="讓我離開語音頻道")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.respond(f'`{ctx.author}` 讓我離開語音頻道 :confused:') # .mention
        print("Bot Command: leave from User {}".format(ctx.author))

    @commands.slash_command(description="撥放音樂(url/搜尋關鍵字)")
    async def play(self, ctx, msg):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.respond("機器人正在撥放音樂 (對列系統還沒寫)")
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
                await ctx.respond('撥放中...')

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
                await ctx.respond('撥放中...')

    @commands.slash_command(description="搜尋YouTube影片")
    async def search(self, ctx, search):
        response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + search + '&key=' + data['yt_api_key'] + '&type=video&maxResults=1')
        jdata = response.json()
        url = "https://www.youtube.com/watch?v=" + jdata['items'][0]['id']['videoId']
        await ctx.respond(url)

# command to resume voice if it is paused
    @commands.slash_command(description="恢復播放")
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.respond('播放已恢復')

    # command to pause voice if it is playing
    @commands.slash_command(description="暫停播放")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.respond('播放已暫停')

    # command to stop voice
    @commands.slash_command(description="停止播放")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.respond('停止撥放...')
        
    """"""

###

    """React"""

##

    """Task"""

def setup(bot):
    bot.add_cog(Slash(bot))