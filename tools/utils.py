from typing import Optional

from tools.logger import logger


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
    "url_numbers": (type(None), int),
    "function_for_message": callable,
    "api_link": str,
    "max_distance_nijmegen": (type(None), int),
    "max_distance_leuven": (type(None), int),
    "query_params": dict,
}


def get_int_from_itemId(item_id: str) -> int:
    return int(item_id[1:])


def convert_transmition(transmission_str: str) -> str:
    transmission_dict = {
        "Handgeschakeld": "manual",
        "Automaat": "automatic",
    }

    if transmission_str and transmission_str in transmission_dict:
        return transmission_dict[transmission_str]
    else:
        return "N/A"


def get_image_url(car: dict) -> Optional[str]:
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
    if type(belgium_price) is not int or type(poland_price) is not int:
        raise TypeError("Both prices should be integers")
    if belgium_price < 200 or poland_price == 0 or model is None or make is None:
        return "N/A"
    elif (
        poland_price > belgium_price * 1.3 and (poland_price - belgium_price * 1.3) > 1000
    ) or poland_price - belgium_price > 2000:
        return "Super Low"
    elif poland_price > belgium_price:
        return "Low"
    else:
        return "High"


def validate_config(config: dict) -> None:
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
