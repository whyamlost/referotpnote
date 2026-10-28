import os
import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


def send_message(chat_id: int, text: str) -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )
    response.raise_for_status()


@app.get("/")
async def health():
    return {"status": "ok", "service": "telegram-starter"}


@app.post("/webhook")
async def webhook(request: Request):
    if not BOT_TOKEN or not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Missing configuration")

    provided_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )
    if provided_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    update = await request.json()
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    message_text = (message.get("text") or "").strip()
    command = message_text.split("@", 1)[0].split(" ", 1)[0].lower()

    if not chat_id:
        return {"ok": True}

    if command == "/start":
        reply = "Welcome! Your bot is online. Send /help to see commands."
    elif command == "/help":
        reply = "Available commands:\n/start - Start the bot\n/help - Show help"
    else:
        reply = "I didn't understand that. Send /start or /help."

    try:
        send_message(chat_id, reply)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Telegram API request failed")

    return {"ok": True}
