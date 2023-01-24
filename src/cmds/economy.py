import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import secrets
from discord.ext.commands import clean_content

time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')

with open('setting.jsonc', mode='r',encoding='utf8') as file:
    data = json.load(file)

with open('cmds/EconomyConfig.json', mode='r',encoding='utf8') as efile:
    edata = json.load(efile)

NEW = edata["NEW"]
Daily_MAX = edata["Daily-MAX"]
Daily_MIN = edata["Daily-MIN"]
Work_MAX = edata["Work-MAX"]
Work_MIN = edata["Work-MIN"]
MAX = edata["MAX"]
MIN = edata["MIN"]

folder = f'cmds/guild'

today = datetime.date.today()

class Economy(Cog_Extension):
    print(f'{time} Economy load!')

    @commands.command(help="建立銀行帳號")
    async def signup(self, ctx):
        guild_economy_folder = str(f'{folder}/{ctx.guild.id}/economy')
        if not os.path.exists(guild_economy_folder):
            os.makedirs(guild_economy_folder)
        filepath = f'{guild_economy_folder}/{ctx.author.id}'
        if os.path.isfile(f'{filepath}.json'):
            await ctx.reply(f"{ctx.author.mention} 你已經有帳號了!!")
        elif not os.path.isfile(f'{filepath}.json'):
            a = await ctx.reply('請稍後, 正在為你建立帳號...')
            with open (f'{filepath}.json',mode="a+",encoding="utf-8") as filt:
                mdata = {"last_time":"0","money": NEW}
                json.dump(mdata, filt, indent=4, ensure_ascii=False)
            await asyncio.sleep(1)
            await a.edit(f"{ctx.author.mention} 帳號建立完成, 你目前有 `{mdata['money']}` 元")
        else:
            await ctx.send("發生錯誤")

    @commands.command(help="每日簽到")
    # @commands.cooldown(rate=1, per=86400, type=commands.BucketType.user)
    async def daily(self, ctx):
        a = await ctx.reply('排隊中...')
        filepath = f'{folder}/{ctx.guild.id}/economy/{ctx.author.id}.json'
        if os.path.isfile(filepath):
            with open(f'{filepath}', mode='r', encoding='utf8') as user:
                udata = json.load(user)
                money = udata['money']
                last_time = udata['last_time']
                if str(today) == str(last_time):
                    await a.edit("你今天已經簽到過了")
                else:
                    up_money = random.randrange(int(Daily_MIN), int(Daily_MAX))
                    new_money = int(money) + int(up_money)
                    udata['money'] = new_money
                    with open(f'{filepath}', mode='w', encoding='utf8') as user:
                        json.dump(udata, user, indent=4, ensure_ascii=False)
                    udata['last_time'] = str(today)
                    with open(f'{filepath}', mode='w', encoding='utf8') as user:
                        json.dump(udata, user, indent=4, ensure_ascii=False)
                        await asyncio.sleep(1)
                    await a.edit(f'本日簽到獎勵: `{up_money}` 元, 你目前有 `{new_money}` 元')
        elif not os.path.isfile(filepath):
            await a.edit(f"{ctx.author.mention} 你沒有帳號,請用 `!signup` 創建一個")
        else:
            await ctx.reply("發生錯誤")

    @commands.command(help="看你有多少錢")
    async def me(self, ctx):
        filepath = f'{folder}/{ctx.guild.id}/economy/{ctx.author.id}.json'
        if os.path.isfile(filepath):
            with open(f'{filepath}', mode='r', encoding='utf8') as me:
                money = json.load(me)
                await ctx.reply(f"你目前有 `{money['money']}` 元")
        elif not os.path.isfile(filepath):
            await ctx.reply(f"{ctx.author.mention}你沒有帳號,請用 `!signup` 創建一個")
        else:
            await ctx.reply("發生錯誤")

    @commands.command(help="領取你一小時的薪水")
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    async def work(self, ctx):
        await ctx.send("功能尚未完成")
        # filepath = f'{folder}/{ctx.guild.id}/economy/{ctx.author.id}.json'
        # if os.path.isfile(filepath):
        #     with open(f'{filepath}', mode='r', encoding='utf8') as user:
        #         udata = json.load(user)
        #     up_money = random.randint(int(Work_MIN), int(Work_MAX))
        #     new_money = int(udata['money']) + int(up_money)
        #     udata['money'] = new_money
        #     with open(f'{filepath}', mode='w', encoding='utf8') as user:
        #         json.dump(udata, user, indent=4, ensure_ascii=False)
        #     await ctx.reply(f'{ctx.message.author.mention}，你賺ㄌ `{up_money}` 元。繼續打工, 一小時後再來\n你目前有 `{new_money}` 元')
        # elif not os.path.isfile(filepath):
        #     await ctx.reply(f"{ctx.author.mention}你沒有帳號,請用 `!signup` 創建一個")
        # else:
        #     await ctx.send("發生錯誤")


    @commands.command(help="猜數字")
    async def guess(self, ctx):
        await ctx.reply("請猜1-100之間的數字(未完成)")
        # ans = random.randint(1, 100)
        # while True:
        #     if num == ans:
        #         await ctx.send("答對了!!")
        #         break
        #     elif num > ans:
        #         await ctx.send("小一點")
        #     elif num < ans:
        #         await ctx.send("大一點")

    @commands.command(name="老虎機", aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if a == b == c:
            await ctx.reply(f"{slotmachine} 全部中獎, 你贏了! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.reply(f"{slotmachine} 連續2次, 你贏了! 🎉")
        else:
            await ctx.reply(f"{slotmachine} 不匹配, 你輸了 😢")

def setup(bot):
    bot.add_cog(Economy(bot))