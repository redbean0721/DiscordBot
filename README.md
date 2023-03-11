[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![Python 3.6](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3108/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)


## :zap: Introduction 簡介

### **Python Discord Bot**

**Pyhon Discord Bot**

一個簡易且基本的Discord機器人

- For 初學者 or 開發者
- Cog 架構, Error Handler, Logger
- Bot指令/斜線命令/類別/功能

<br>

## :inbox_tray: Installation 安裝指南
> 運行環境 建議 `Python 3.10` / `discord.py 2.1.0` / `Pycord 2.3.3` 以上(含)

1. 下載並解壓整個專案
2. 安裝 `Python 3.10`
3. 在 DiscordBot 資料夾運行 `pip install -r requirements.txt`
3. 打開 src 資料夾將 `example.env` 重新命名為 `.env` 並將機器人TOKEN填入
4. 將 `example_setting.json` 重新命名為 `setting.json` 並自行修改檔案裡的資料
5. 將 ffmpeg 複製到 Python Scripts 資料夾內(此為音樂撥放部分可忽略)
6. 運行 `python bot.py`

<br>

## :nut_and_bolt: Folder structure 資料夾結構
```
/ # 根目錄
------------------------------------
- .env # 機器人TOKEN
- bot.py # bot 啟動主程式
- setting.json # 設定檔
- version.json # 機器人版本


/cmds # 放置所有 Cog 指令
------------------------------------
- admin.py  # 管理用指令(皆須有權限才可使用)
- economy.py  # 經濟指令
- event.py  # 所有觸發性事件區
- fun.py    # 娛樂用途指令
- main.py   # 主要指令區
- music.py  # 音樂功能
- react.py  # 反映事件
- slash.py  # 所有斜線命令
- task.py   # 定時任務 (未完成)


/modules # 放置所有模組
------------------------------------
StatusChanger.py  # 機器人狀態定時變更
DirectMessages.py # 使用機器人私訊成員 (未完成)


/core  #放置類別、核心通用功能
------------------------------------
- classes.py # 主要類別區
