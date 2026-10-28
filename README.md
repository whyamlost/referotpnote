# Safe Telegram Bot Starter (Render)

A minimal FastAPI webhook bot with `/start` and `/help` only.

## Deploy on Render
1. Upload these files to a NEW GitHub repository.
2. In Render, choose **New + → Web Service** and select the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn api.index:app --host 0.0.0.0 --port $PORT`
5. In Render Environment, add:
   - `TELEGRAM_BOT_TOKEN`: your bot token from @BotFather
   - `WEBHOOK_SECRET`: a unique random string of 32+ characters
6. Deploy and open `https://your-service.onrender.com/`; it should return JSON with `status: ok`.

## Telegram webhook
Webhook URL: `https://your-service.onrender.com/webhook`
Use the same secret as the `WEBHOOK_SECRET` environment variable for Telegram's `secret_token` parameter.
Never publish your token or secret in GitHub or screenshots.

This starter handles only `/start` and `/help`. It does not collect phone numbers, extract SMS/OTP codes, or sync sensitive records.
