import discord
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os, time, datetime, random, logging, requests
import json, yaml
import secrets
from discord.ext.commands import clean_content

with open('setting.json', mode='r',encoding='utf8') as file:
    data = json.load(file)

class Fun(Cog_Extension):
    time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S INFO]:')
    print(f'{time} Fun load!')

    @commands.command(help="")
    async def f(self, ctx, *, text: clean_content = None):
        """ 按 F 表達敬意 """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command(help="擲硬幣")
    async def coin_flip(self, ctx):
        coin_sides = ['正面', '反面']
        await ctx.send(f"{ctx.author.name} 擲硬幣得到 **{random.choice(coin_sides)}**!")

    @commands.command(name="反轉", aliases=["reverse"])
    async def reverse(self, ctx, *, text: str):
        """ !轉反會都入輸有所
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(help="隨機回傳一個百分比來代表一個人有多 hot")
    async def hot_calc(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(help="給某人一杯啤酒! 🍻")
    async def beer(self, ctx, user: discord.Member = None, *, reason: clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*陪你喝啤酒* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, 你收到了 **{ctx.author.name}** 的 🍺"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** 和 **{ctx.author.name}** 正在一起享用美味的啤酒 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"好吧, 看起來 **{user.name}** 不想和 **{ctx.author.name}** 你喝啤酒 ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, 你收到了來自 **{ctx.author.name}** 的 🍺"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

def setup(bot):
    bot.add_cog(Fun(bot))