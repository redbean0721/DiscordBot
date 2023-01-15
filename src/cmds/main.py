import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import secrets

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Main(Cog_Extension):
    print(f'{time} Main load!')

    @commands.command(help="跟你say Hellow")
    async def hi(self, ctx):
        # hi = ['誰叫我', '我在這~', '怎麼了', '?']
        await ctx.reply(random.choice(['誰叫我', '我在這~', '怎麼了', '?']))

    @commands.command(help="ping我看我ㄉ延遲")
    async def ping(self, ctx):
        await ctx.send(f'機器人延遲 {round(self.bot.latency*1000)} ms\nAPI延遲 {round(self.bot.ws.latency*1000)} ms')

    @commands.command(help="讓我幫你說話")
    async def say(self, ctx, msg):
        if msg != ("@everyone") and msg != ("@here"):
            await ctx.message.delete()
            async with ctx.typing():
                await asyncio.sleep(4)
            await ctx.send(msg)
        else:
            await ctx.reply(f'<@{ctx.message.author.id}> 你不可以tag everyone或here!!')
    
    @commands.command(help="讓我私訊使用者")
    async def dm(self, msg, member: discord.Member):
        await member.send(msg)

    @commands.command(help="清除訊息")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.send(f'<@{ctx.message.author.id}> 已刪除 {num} 則訊息')

    @commands.command(help="隨機生成一串密碼")
    async def password(self, ctx, n_bytes: int = 18):
        if n_bytes not in range(3, 1401):
            return await ctx.respond("請輸入 3-1400 內的數字")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.reply(f"密碼已發送至您的私人訊息")
        await ctx.author.send(f"🎁 **這是您的密碼:**\n```{secrets.token_urlsafe(n_bytes)}```")

    @commands.command(help="關於我")
    async def info(self, ctx):
        embed=discord.Embed(title="關於我", description=f'{self.bot.user}', color=0x00fbff, timestamp= datetime.datetime.now())
        embed.add_field(name="開發者 Developers", value="redbean0721#5582", inline=False)
        embed.add_field(name="源碼 Source", value="https://github.com/redbean0721/DiscordBot", inline=False)
        embed.add_field(name="協助 Support Server", value="https://discord.gg/9hwuNYXA4q", inline=True)
        embed.add_field(name="版本 Version", value="1.0", inline=False)
        embed.add_field(name="使用語言", value="discord.py", inline=True)
        embed.add_field(name="指令 Prefix", value=(data['prefix']), inline=False)
        embed.add_field(name="服務中的伺服器 Server count", value=f"{len(self.bot.guilds)}", inline=False)
        embed.add_field(name="機器人延遲", value=f'{round(self.bot.latency*1000)} ms', inline=False)
        embed.add_field(name="API延遲", value=f'{round(self.bot.ws.latency*1000)} ms', inline=False)
        embed.set_footer(text="Made with ❤")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Main(bot))