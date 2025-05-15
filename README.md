# Telegram 算命机器人

## 简介

这是一个基于 Flask 的 Telegram 机器人示例，包含简单的星座、八字、塔罗命令响应示例，接入 OpenAI 可扩展。

## 运行

1. 设置环境变量：
   - TELEGRAM_TOKEN=你的 Telegram Bot Token
   - OPENAI_API_KEY=你的 OpenAI API Key

2. 启动：
```
pip install -r requirements.txt
python main.py
```

3. 设置 Telegram webhook 指向你的公网地址 `/webhook` 路径。

## 功能

- /start 欢迎信息
- /zodiac 星座运势
- /bazi 八字解析（示例）
- /tarot 塔罗牌抽取（示例）