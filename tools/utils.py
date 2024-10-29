import re
import json
import requests
from typing import Optional
from geopy.distance import geodesic
from deep_translator import GoogleTranslator

from tools.logging import logger

NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)
HERENT = (50.9093, 4.6774)

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


def send_telegram_message(
    bot_token: str,
    admin_id: int,
    message: str,
    image_url: str = None,
    two_dehands_url: str = None,
    otomoto_url: str = None,
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


def translate_to_english(text):
    try:
        translated_text = translator_en.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        translated_text = text
    return translated_text


def translate_to_russian(text):
    try:
        translated_text = translator_ru.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        logger.error(f"Error in translation: {e}")
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


def extract_gearbox_from_ad(text: str) -> str:
    manual_keywords = [
        "handgeschakeld",
        "handgeschakelde",
        "manueel",
        "manual",
        "manuell",
        "manuale",
        "boîte manuelle",
        "schaltgetriebe",
        "mécanique",
    ]
    automatic_keywords = [
        "automaat",
        "automat",
        "automatic",
        "automatik",
        "automatico",
        "boîte automatique",
        "automatique",
        "automatische",
        "automatisch",
    ]
    exclusion_keywords = [
        "phare",
        "essuie",
        "essuie-glace",
        "lumière",
        "lichten",
        "airconditioning",
        "laser",
        "anti",
        "feux",
        "light",
        "wiper",
        "airco",
    ]

    text = text.lower()

    # Combine keywords into regular expressions with boundary checking
    manual_pattern = r"\b(?:" + "|".join(manual_keywords) + r")\b"
    automatic_pattern = r"\b(?:" + "|".join(automatic_keywords) + r")\b"
    exclusion_pattern = r"\b(?:" + "|".join(exclusion_keywords) + r")\b"

    # Ensure "automatic" keywords do not appear next to exclusion keywords
    if re.search(automatic_pattern, text):
        if not re.search(rf"{exclusion_pattern}\s+{automatic_pattern}|{automatic_pattern}\s+{exclusion_pattern}", text):
            return "automatic"

    # Ensure "manual" keywords are detected without restriction
    if re.search(manual_pattern, text):
        return "manual"

    return "N/A"


def extract_fuel_type_from_ad(text: str) -> str:
    petrol_keywords = [
        "petrol",
        "gasoline",
        "gas",
        "essence",
        "benzine",
        "benzin",
        "benzina",
        "gti",
        "tce",
        "fsi",
        "tfsi",
        "tsi",
    ]
    diesel_keywords = [
        "diesel",
        "gtd",
        "tdi",
        "dci",
        "cdti",
        "hdi",
        "cddi",
        "d4d",
    ]
    hybrid_keywords = ["hybrid", "hybride"]

    text = text.lower()

    petrol_pattern = r"\b(?:" + "|".join(petrol_keywords) + r")\b"
    diesel_pattern = r"\b(?:" + "|".join(diesel_keywords) + r")\b"
    hybrid_pattern = r"\b(?:" + "|".join(hybrid_keywords) + r")\b"

    if re.search(hybrid_pattern, text):
        return "Hybrid"
    elif re.search(diesel_pattern, text):
        return "Diesel"
    elif re.search(petrol_pattern, text):
        return "Benzine"
    else:
        return "N/A"


def convert_transmition(transmission_str: str):
    transmission_dict = {
        "Handgeschakeld": "manual",
        "Automaat": "automatic",
    }

    if transmission_str and transmission_str in transmission_dict:
        return transmission_dict[transmission_str]
    else:
        return "N/A"


def get_image_url(car: dict):
    pictures = car.get("pictures", [])

    if pictures:
        first_image = pictures[0]
        return first_image.get("extraExtraLargeUrl", None)
    else:
        return None


def get_price_info(
    belgium_price: int,
    poland_price: int,
    make: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    if belgium_price == 0 or poland_price == 0 or model is None or make is None:
        return "N/A"
    elif poland_price > belgium_price * 1.3:
        return "Super Low"
    elif poland_price > belgium_price:
        return "Low"
    else:
        return "High"


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

    logger.info(f"Configuration for {config['source']} is valid")
