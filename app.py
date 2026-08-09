from fastapi import FastAPI, Request
import os
import requests
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


@app.get("/")
def home():
    return {"status": "TradingView AI Telegram is running"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    symbol = data.get("symbol", "Unknown")
    price = data.get("price", "Unknown")
    signal = data.get("signal", "Unknown")
    timeframe = data.get("timeframe", "Unknown")

    prompt = f"""
You are a trading analysis assistant.

TradingView alert:
Symbol: {symbol}
Price: {price}
Timeframe: {timeframe}
Signal: {signal}

Give a concise analysis in Malay.

Include:
1. Signal
2. Market interpretation
3. Entry consideration
4. Stop loss consideration
5. Take profit consideration
6. Risk warning

Do not guarantee profit.
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    analysis = response.output_text

    message = f"""
📊 TRADINGVIEW ALERT

Symbol: {symbol}
Price: {price}
Timeframe: {timeframe}
Signal: {signal}

🤖 AI ANALYSIS

{analysis}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
    )

    return {"status": "sent"}