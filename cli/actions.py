from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable
import threading
import os
import time
from pathlib import Path

import yaml
import discord
from discord.ext import commands


@dataclass(frozen=True)
class CliCommand:
    name: str
    description: str
    usage: str
    group: str
    handler: Callable[[commands.Bot, list[str], threading.Event, dict[str, CliCommand]], None]


def stop_bot(bot: commands.Bot):
    print("正在停止機器人...")
    if bot.loop.is_running():
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)


def restart_bot(bot: commands.Bot, restart_requested: threading.Event):
    print("正在重啟機器人...")
    restart_requested.set()
    if bot.loop.is_running():
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)


def load_extension(bot: commands.Bot, extension: str):
    coroutine = bot.load_extension(f"cogs.{extension}")
    future = asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
    future.result()
    print(f"已load cogs.{extension}")


def unload_extension(bot: commands.Bot, extension: str):
    coroutine = bot.unload_extension(f"cogs.{extension}")
    future = asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
    future.result()
    print(f"已unload cogs.{extension}")


def reload_extension(bot: commands.Bot, extension: str):
    coroutine = bot.reload_extension(f"cogs.{extension}")
    future = asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
    future.result()
    print(f"已reload cogs.{extension}")


def ban_user(bot: commands.Bot, guild_id: int, user_id: int, reason: str | None = None):
    future = asyncio.run_coroutine_threadsafe(_ban_user(bot, guild_id, user_id, reason), bot.loop)
    future.result()
    print(f"已封鎖 user_id={user_id} in guild_id={guild_id}")


async def _ban_user(
    bot: commands.Bot,
    guild_id: int,
    user_id: int,
    reason: str | None = None,
):
    guild = bot.get_guild(guild_id)
    if guild is None:
        raise ValueError(f"找不到 Guild: {guild_id}")

    await guild.ban(discord.Object(id=user_id), reason=reason)


def handle_stop(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    stop_bot(bot)


def handle_restart(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    restart_bot(bot, restart_requested)


def handle_load(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    if not arguments:
        print(f"用法: {registry['load'].usage}")
        return

    try:
        load_extension(bot, arguments[0])
    except Exception as error:
        print(f"load 失敗: {error}")


def handle_unload(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    if not arguments:
        print(f"用法: {registry['unload'].usage}")
        return

    try:
        unload_extension(bot, arguments[0])
    except Exception as error:
        print(f"unload 失敗: {error}")


def handle_reload(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    if not arguments:
        print(f"用法: {registry['reload'].usage}")
        return

    try:
        reload_extension(bot, arguments[0])
    except Exception as error:
        print(f"reload 失敗: {error}")


def handle_ban(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    if len(arguments) < 2:
        print(f"用法: {registry['ban'].usage}")
        return

    try:
        guild_id = int(arguments[0])
        user_id = int(arguments[1])
    except ValueError:
        print("guild_id 和 user_id 必須是整數")
        return

    reason = " ".join(arguments[2:]) if len(arguments) > 2 else None

    try:
        ban_user(bot, guild_id, user_id, reason)
    except Exception as error:
        print(f"ban 失敗: {error}")


def render_help(registry: dict[str, CliCommand]) -> str:
    grouped: dict[str, list[CliCommand]] = {}
    for command in registry.values():
        grouped.setdefault(command.group, []).append(command)

    lines: list[str] = ["CLI 指令列表"]
    group_order = ["基礎", "管理", "其他"]

    for group_name in group_order:
        commands_in_group = grouped.pop(group_name, [])
        if not commands_in_group:
            continue

        lines.append(f"\n{group_name}:")
        for command in commands_in_group:
            lines.append(f"  {command.name:<8} {command.description}")
            lines.append(f"    用法: {command.usage}")

    for group_name, commands_in_group in grouped.items():
        lines.append(f"\n{group_name}:")
        for command in commands_in_group:
            lines.append(f"  {command.name:<8} {command.description}")
            lines.append(f"    用法: {command.usage}")

    return "\n".join(lines)


def handle_help(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    print(render_help(registry))


start_time = time.time()


def handle_status(bot: commands.Bot, arguments: list[str], restart_requested: threading.Event, registry: dict[str, CliCommand]):
    pid = os.getpid()
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    user_count = len(bot.users) if bot.users else 0
    guild_count = len(bot.guilds) if bot.guilds else 0
    is_ready = bot.user is not None
    
    threads = threading.enumerate()
    thread_info = "\n".join([f"    - {t.name} (daemon={t.daemon})" for t in threads])
    
    print(f"""
Bot 狀態:
  PID: {pid}
  Uptime: {uptime_str}
  Connected: {is_ready}
  Guilds: {guild_count}
  Users: {user_count}

執行緒 ({len(threads)} 個):
{thread_info}
""")


HANDLER_MAP = {
    "handle_stop": handle_stop,
    "handle_restart": handle_restart,
    "handle_load": handle_load,
    "handle_unload": handle_unload,
    "handle_reload": handle_reload,
    "handle_ban": handle_ban,
    "handle_help": handle_help,
    "handle_status": handle_status,
}


def load_cli_config() -> dict[str, CliCommand]:
    config_path = Path(__file__).parent.parent / "cli.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    commands: dict[str, CliCommand] = {}
    for name, cmd_config in config.get("commands", {}).items():
        handler_name = cmd_config.get("handler")
        handler = HANDLER_MAP.get(handler_name)
        if handler is None:
            raise ValueError(f"Handler not found: {handler_name}")
        
        commands[name] = CliCommand(
            name=name,
            description=cmd_config["description"],
            usage=cmd_config["usage"],
            group=cmd_config["group"],
            handler=handler,
        )
    return commands


CLI_COMMANDS = load_cli_config()
