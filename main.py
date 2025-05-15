import os
from flask import Flask, request, jsonify
import requests
import openai
import random

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise Exception("请设置 TELEGRAM_TOKEN 和 OPENAI_API_KEY 环境变量")

BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
openai.api_key = OPENAI_API_KEY

TAROT_CARDS = [
    "正位·愚人：新的开始、冒险",
    "逆位·魔术师：欺骗、误导",
    "正位·恋人：爱情、和谐",
    "正位·战车：胜利、掌控",
    "逆位·塔：突然的变化、崩溃",
    "正位·星星：希望、灵感"
]

def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

def gpt_reply(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message['content']
    except Exception as e:
        return f"AI出错：{e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "欢迎使用算命机器人！
请输入 /zodiac 查看星座运势
/bazi 八字分析
/tarot 抽一张塔罗牌")
        elif text.startswith("/zodiac"):
            reply = gpt_reply("请用简洁的中文写一段今日星座运势，积极正面，100字内")
            send_message(chat_id, reply)
        elif text.startswith("/bazi"):
            send_message(chat_id, "请输入出生年月日时，例如：1992年7月15日 09:00")
        elif text.startswith("/tarot"):
            send_message(chat_id, f"塔罗牌抽取结果：{random.choice(TAROT_CARDS)}")
        else:
            send_message(chat_id, "命令未识别，请输入 /start 获取帮助。")
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)