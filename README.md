[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![Python 3.6](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3108/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)


## :zap: Introduction 簡介

### **Discord Python Bot**

**Discord Pyhon Bot**

提供一個乾淨的基本骨架，快速的開始一隻新的機器人開發

- For (初學者/開發者)
- Cog 架構
- Bot指令/斜線命令/類別/功能 分離
- Error Handler 、 Logger 、 Gloable Function 、 Checker

<br>

## :inbox_tray: Installation 安裝指南
> 運行環境 建議 `Python 3.10` / `discord.py 2.1` / `Pycord 2.2.3` 以上(含)

1. 下載整個專案
2. 安裝 `Python 3.10`
3. 解壓後自行修改設定檔 `setting.json` 裡的資料
4. 在終端機執行 `pip install discord.py` 和 `pip install -U git+https://github.com/Pycord-Development/pycord`
5. 運行 `python bot.py`

<br>

## :nut_and_bolt: Folder structure 資料夾結構
```
/ # 根目錄
------------------------------------
- bot.py # bot 啟動主程式
- setting.json # 設定檔


/cmds # 放置所有 Cog 指令
------------------------------------
- main.py  #主要指令區
- event.py # 所有 event 觸發性事件指令區
- music.py # 音樂功能指令區


/core  #放置類別、核心通用功能
------------------------------------
- classes.py # 主要類別區
- check.py # 自定全域指令檢查器
- error.py # 預設、自訂 錯誤管理器
```
