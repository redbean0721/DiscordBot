import threading
from pathlib import Path

import yaml
from discord.ext import commands

from cli.actions import CLI_COMMANDS


def load_command_aliases() -> dict[str, str]:
    config_path = Path(__file__).parent.parent / "cli.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("aliases", {})


COMMAND_ALIASES = load_command_aliases()


def run_cli(bot: commands.Bot, restart_requested: threading.Event, startup_ready: threading.Event):
    startup_ready.wait()
    print("CLI 已啟動，輸入 help 可查看所有指令")

    while True:
        try:
            raw = input("cli> ").strip()
        except EOFError:
            raw = "stop"
        except KeyboardInterrupt:
            raw = "stop"

        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()
        arguments = parts[1:]

        command = COMMAND_ALIASES.get(command, command)
        command_spec = CLI_COMMANDS.get(command)
        if command_spec is None:
            print(f"command not found: {command}")
            continue

        command_spec.handler(bot, arguments, restart_requested, CLI_COMMANDS)

        if command == "stop" or command == "restart":
            break
