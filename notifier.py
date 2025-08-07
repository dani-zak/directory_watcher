import requests
from config import BOT_TOKEN, CHAT_ID

def send_telegram_message(message: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id":    CHAT_ID,
        "parse_mode": "Markdown",
        "text":       message
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
