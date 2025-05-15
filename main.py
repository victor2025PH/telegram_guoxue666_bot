import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise Exception("请设置 TELEGRAM_TOKEN 和 OPENAI_API_KEY 环境变量")

BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "欢迎使用算命机器人！请输入 /zodiac 查看星座运势，/bazi 查看八字，/tarot 抽塔罗牌。")
        elif text.startswith("/zodiac"):
            # 简单模拟回复
            send_message(chat_id, "今日星座运势：好运连连！")
        elif text.startswith("/bazi"):
            send_message(chat_id, "八字解析功能开发中。")
        elif text.startswith("/tarot"):
            send_message(chat_id, "塔罗牌抽取：正位愚人，代表新开始。")
        else:
            send_message(chat_id, "命令未识别，请输入 /start 获取帮助。")
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)