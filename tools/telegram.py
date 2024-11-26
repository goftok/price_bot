import json
import requests
from typing import Optional

from tools.logger import logger


def send_telegram_message(
    bot_token: str,
    admin_id: int,
    message: str,
    image_url: Optional[str] = None,
    two_dehands_url: Optional[str] = None,
    autoscout24_url: Optional[str] = None,
    otomoto_url: Optional[str] = None,
):
    if image_url:
        base_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    else:
        base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    if image_url:
        payload = {
            "chat_id": admin_id,
            "photo": image_url,
            "caption": message,
            "parse_mode": "HTML",
        }
    else:
        payload = {"chat_id": admin_id, "text": message, "parse_mode": "HTML"}

    buttons = []

    if two_dehands_url:
        buttons.append({"text": "2dehands", "url": two_dehands_url})

    if autoscout24_url:
        buttons.append({"text": "Autoscout24", "url": autoscout24_url})

    if otomoto_url:
        buttons.append({"text": "Otomoto", "url": otomoto_url})

    if buttons:
        inline_keyboard = {"inline_keyboard": [buttons]}
        payload["reply_markup"] = json.dumps(inline_keyboard)

    try:
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {e}")
        return {"error": str(e)}
