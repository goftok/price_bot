import re
import requests
from rich.console import Console
from geopy.distance import geodesic
from deep_translator import GoogleTranslator

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
    "min_year": (type(None), int),
    "max_year": (type(None), int),
    "min_mileage": (type(None), int),
    "max_mileage": (type(None), int),
    "chat_id": str,
    "not_allowed_models": (type(None), list),
    "allowed_models": (type(None), list),
    "is_automatic_transmission": (type(None), bool),
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


def get_int_from_itemId(item_id: str):
    return int(item_id[1:])


def extract_year_from_ad(text: str) -> str:
    MIN_YEAR = 1980
    MAX_YEAR = 2025

    # Use regex to find all sequences of four digits in the text
    potential_years = re.findall(r"\b(19[8-9]\d|20[0-2]\d)\b", text)

    # Iterate through the found years and return the first one within the valid range
    for year in potential_years:
        year = int(year)
        if MIN_YEAR <= year <= MAX_YEAR:
            return str(year)

    # If no valid year is found, return None
    return None


def extract_mileage_from_ad(text: str) -> str:
    # Regex pattern to capture mileage between 10,000 and 999,999
    main_regex = r"\b(?:\d{1,3}[.,])?\d{1,3}[.,]?\d{3}\s*(?:km|kms|KM|Km|Kms|KMs|kilometers|kilometres|k m)?\b"

    spaced_regex = r"\b\d{1,3}\s\d{3}\s*(?:km|kms|KM|Km|Kms|KMs|kilometers|kilometres|k m)?\b"

    # Try to extract mileage using the main regex pattern
    mileage = extract_mileage_using_regex(main_regex, text)

    # If no mileage is found, try to extract mileage using the spaced regex pattern
    if mileage is None:
        mileage = extract_mileage_using_regex(spaced_regex, text)

    return mileage


def extract_mileage_using_regex(regex: str, text: str) -> str:
    mileage_pattern = re.compile(regex, re.IGNORECASE)
    matches = mileage_pattern.findall(text)

    for match in matches:
        clean_mileage = re.sub(r"[^\d]", "", match)
        if 10000 <= int(clean_mileage) <= 999999:
            return str(int(clean_mileage))

    return None


def convert_transmition(transmission_str: str):
    transmission_dict = {
        "Handgeschakeld": "manual",
        "Automaat": "automatic",
    }

    if transmission_str and transmission_str in transmission_dict:
        return transmission_dict[transmission_str]
    else:
        return "N/A"


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

    extra_keys = [key for key in config if key not in template_config]
    if extra_keys:
        raise ValueError(f"Extra keys found in configuration: {extra_keys}")

    console.print(f"Configuration for {config['source']} is valid")
