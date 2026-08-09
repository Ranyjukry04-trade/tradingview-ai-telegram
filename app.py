from flask import Flask, request
import telegram
import os

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = f"🚨 TradingView Alert 🚨\n\n{data}"
    bot.send_message(chat_id=CHAT_ID, text=message)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
