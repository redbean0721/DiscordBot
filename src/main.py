from dotenv import load_dotenv
import discord
import json
import os


load_dotenv()

version = json.load(open("version.json", "r"))["version"]

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="機器人整修中..."), status=discord.Status.dnd)
    print(f"Logged in: {bot.user} | {bot.user.id}")
    print(f"Version: {version}")


async def main():
    async with bot:
        await bot.start(os.getenv("TOKEN"))
