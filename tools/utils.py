import requests
from rich.console import Console
from geopy.distance import geodesic
from deep_translator import GoogleTranslator
from tools.secrets import BOT_TOKEN, CHAT_ID1, CHAT_ID2, CHAT_ID3

NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)
HERENT = (50.9093, 4.6774)

console = Console()
translator_en = GoogleTranslator(source="auto", target="en")
translator_ru = GoogleTranslator(source="auto", target="ru")

template_config = {
    "source": str,
    "min_price": (type(None), int),
    "max_price": (type(None), int),
    "chat_id": str,
    "allowed_models": (type(None), list),
    "url_numbers": int,
    "function_for_message": callable,
    "api_link": str,
    "max_distance_nijmegen": (type(None), int),
    "max_distance_leuven": (type(None), int),
    "query_params": dict,
}


def calculate_driving_distance(origin: tuple, destination: tuple):
    return geodesic(origin, destination).kilometers


def send_telegram_message(bot_token: str, admin_id: int, message: str):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(base_url, data=payload)
    return response.json()


def translate_to_english(text):
    try:
        translated_text = translator_en.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        console.log(f"Error in translation: {e}")
        translated_text = text
    return translated_text


def translate_to_russian(text):
    try:
        translated_text = translator_ru.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        console.log(f"Error in translation: {e}")
        translated_text = text
    return translated_text


def create_urls(config: dict, limit: int = 100):
    urls = []
    for i in range(config["url_numbers"]):
        query_params = config["query_params"].copy()
        query_params["offset"] = i * limit
        query_params["limit"] = limit

        # Handling list values in query parameters
        query_string_parts = []
        for key, value in query_params.items():
            if isinstance(value, list):
                for v in value:
                    query_string_parts.append(f"{key}[]={str(v)}")
            else:
                query_string_parts.append(f"{key}={str(value)}")

        query_string = "&".join(query_string_parts)
        url = f"{config['api_link']}?{query_string}"
        urls.append(url)

    return urls


def send_errors_to_all_chats(e: Exception):
    for chat_id in [CHAT_ID1, CHAT_ID2, CHAT_ID3]:
        send_telegram_message(BOT_TOKEN, chat_id, f"bot error: {e}")


def get_int_from_itemId(item_id: str):
    return int(item_id[1:])


def validate_config(config):
    for t_key, t_value in template_config.items():
        if t_key not in config:
            raise ValueError(f"Key '{t_key}' missing in configuration")

        if t_key == "function_for_message":
            if not callable(config[t_key]):
                raise TypeError(f"The '{t_key}' should be a callable (function). Got: {type(config[t_key]).__name__}")
        else:
            if t_key == "query_params":
                for q_key, q_value in config[t_key].items():
                    if not isinstance(q_value, (list, str)):
                        raise TypeError(
                            f"Incorrect type for key '{q_key}'. Expected list or str, got {type(q_value).__name__}"
                        )

            if not isinstance(config[t_key], t_value):
                raise TypeError(
                    f"Incorrect type for key '{t_key}'. Expected {t_value.__name__}, "
                    f"got {type(config[t_key]).__name__}"
                )
    console.print(f"Configuration for {config['source']} is valid")
