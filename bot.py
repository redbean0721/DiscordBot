import discord
from discord.ext import commands
import asyncio, os, sys, threading

from cli import run_cli

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
startup_ready = threading.Event()

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份: {bot.user}")
    print(f"已同步 {len(slash)} 個指令")
    startup_ready.set()

# 載入指令程式檔案
@bot.tree.command(name="load", description="載入 Cog 模組")
@commands.is_owner()
async def load(interaction: discord.Interaction, extension: str):
    try:
        await bot.load_extension(f"cogs.{extension}")
        await interaction.response.send_message(f"已載入 {extension} 模組", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"載入失敗: {e}", ephemeral=True)

# 卸載指令檔案
@bot.tree.command(name="unload", description="卸載 Cog 模組")
@commands.is_owner()
async def unload(interaction: discord.Interaction, extension: str):
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await interaction.response.send_message(f"已卸載 {extension} 模組", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"卸載失敗: {e}", ephemeral=True)

# 重新載入程式檔案
@bot.tree.command(name="reload", description="重新載入 Cog 模組")
@commands.is_owner()
async def reload(interaction: discord.Interaction, extension: str):
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await interaction.response.send_message(f"已重新載入 {extension} 模組", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"重新載入失敗: {e}", ephemeral=True)

# 幫助指令
@bot.tree.command(name="help", description="顯示所有可用指令")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="指令列表", color=discord.Color.blue())
    
    # 動態新增所有公開指令
    for command in bot.tree.get_commands():
        if command.name != "help" and command.name not in ["load", "unload", "reload"]:
            raw_description = getattr(command, "description", None)
            description = raw_description if isinstance(raw_description, str) and raw_description else "沒有描述"
            embed.add_field(name=f"/{command.name}", value=description, inline=False)
    
    # 只給擁有者顯示管理指令
    if await bot.is_owner(interaction.user):
        embed.add_field(name="**=== 管理指令 ===", value="(只有擁有者可見)", inline=False)
        for command in bot.tree.get_commands():
            if command.name in ["load", "unload", "reload"]:
                raw_description = getattr(command, "description", None)
                description = raw_description if isinstance(raw_description, str) and raw_description else "沒有描述"
                embed.add_field(name=f"/{command.name}", value=description, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# 一開始bot開機需載入全部程式檔案
async def load_all_extensions():
    for root, _dirs, files in os.walk("./cogs"):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                module_path = os.path.join(root, filename)[2:-3].replace(os.sep, ".")
                await bot.load_extension(module_path)
                print(f"已載入 Cog: {module_path}")

restart_requested = threading.Event()


async def main():
    token = os.getenv("BOT_TOKEN")
    if token is None:
        raise RuntimeError("缺少環境變數 BOT_TOKEN")
    
    await load_all_extensions()
    cli_thread = threading.Thread(target=run_cli, args=(bot, restart_requested, startup_ready), daemon=True)
    cli_thread.start()

    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n正在關閉機器人...")
    finally:
        if restart_requested.is_set():
            print("正在重新啟動程式...")
            os.execv(sys.executable, [sys.executable] + sys.argv)