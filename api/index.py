import os
import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Recommended: set these in Render Environment Variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


def send_message(chat_id: int, text: str):
    if not BOT_TOKEN:
        raise RuntimeError("Telegram bot token is not configured")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )
    response.raise_for_status()


@app.get("/")
def home():
    return {"status": "ok", "bot": "running"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    supplied_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )
    if supplied_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    update = await request.json()
    message = update.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip()

    if not chat_id:
        return {"ok": True}

    if text == "/start":
        send_message(chat_id, "Hello! Your Telegram bot is working.")
    elif text == "/help":
        send_message(chat_id, "Available commands:\n/start - Start the bot\n/help - Help")

    return {"ok": True}
