[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![Python 3.6](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3108/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)


## :zap: Introduction 簡介

### **Discord Python Bot**

**Discord Pyhon Bot**

提供一個簡易且基本的機器人以開發

- For 初學者 or 開發者
- Cog 架構
- Bot指令/斜線命令/類別, 分離/功能
- Error Handler 、 Logger 、 Gloable Function 、 Checker

<br>

## :inbox_tray: Installation 安裝指南
> 運行環境 建議 `Python 3.10` / `discord.py 2.1.0` / `Pycord 2.3.3` 以上(含)

1. 下載整個專案
2. 安裝 `Python 3.11`
3. 將 `example.env` 重新命名為 `.env` 並將機器人TOKEN填入
4. 解壓後將 `example_setting.json` 重新命名為 `setting.json` 並自行修改檔案裡的資料
5. 在終端機執行 `pip install discord.py` 和 `pip install -U git+https://github.com/Pycord-Development/pycord`
6. 運行 `python bot.py`

<br>

## :nut_and_bolt: Folder structure 資料夾結構
```
/ # 根目錄
------------------------------------
- bot.py # bot 啟動主程式
- setting.json # 設定檔
- .env # 機器人TOKEN


/cmds # 放置所有 Cog 指令
------------------------------------
- admin.py  # 管理用指令(皆須有權限才可使用)
- economy.py  # 經濟指令
- event.py  # 所有 event 觸發性事件指令區
- fun.py    # 娛樂用途指令
- main.py   # 主要指令區
- music.py  # 音樂功能
- react.py  # 反映事件
- slash.py  # 所有斜線命令
- task.py   # 定時任務


/modules # 放置所有模組
------------------------------------
StatusChanger.py  # 機器人狀態定時變更
DirectMessages.py # 使用機器人私訊成員


/core  #放置類別、核心通用功能
------------------------------------
- classes.py # 主要類別區
