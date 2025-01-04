import time
import requests
from typing import Optional, Tuple

from tools.secrets import BOT_TOKEN
from tools.logger import logger
from tools.telegram import send_telegram_message
from tools.secrets import send_errors_to_all_chats


ERROR_CODES = [403, 404, 500, 502]  # 429
MIN_WAIT_TIME = 10.1  # seconds
RETRY_TIMES = 5
MAX_ID_LOOKUP = 100


def create_autoscout24_url(config: dict) -> str:
    """
    Attempts to construct a valid AutoScout24 URL by iterating over a range of IDs,
    then returns the first URL that responds with status 200.
    Raises an exception if no valid URL is found.
    """
    start_id = config["start_id"]
    api_link = config["api_link"]
    query_params = config["query_params"].copy()

    def try_url_with_retries(url: str) -> bool:
        """
        Attempt to GET `url` up to RETRY_TIMES if status is in ERROR_CODES.
        Sleeps between attempts. Returns True if a 200 status is eventually reached.
        """
        for attempt in range(RETRY_TIMES):
            response = requests.get(url)
            if response.status_code == 200:
                return True
            if response.status_code not in ERROR_CODES:
                return False
            time.sleep(MIN_WAIT_TIME)
        return False

    def get_correct_id_url(query_string: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Iterates over up to MAX_ID_LOOKUP IDs to find a valid (URL, ID).
        Returns (None, None) if not found.
        """
        for i in range(MAX_ID_LOOKUP):
            current_id = start_id + i
            url = f"{api_link}/as24-search-funnel_main-{current_id}/lst.json?{query_string}"
            if try_url_with_retries(url):
                return url, current_id
        return None, None

    query_string_parts = []
    for key, value in query_params.items():
        if isinstance(value, list):
            for v in value:
                query_string_parts.append(f"{key}[]={str(v)}")
        else:
            query_string_parts.append(f"{key}={str(value)}")

    query_string = "&".join(query_string_parts)

    # Attempt to find the correct URL
    url, start_id = get_correct_id_url(query_string)
    if url is None or start_id is None:
        source = config["source"]
        raise Exception(f"Could not find correct id for url for {source}")

    config["start_id"] = start_id
    config["urls"] = url

    logger.info(f"Found last id for '{config['source']}': {start_id}")
    return url, start_id


def get_ads(url: str, ad_config: dict) -> list:
    try:
        response = requests.get(url)
        if response.status_code in ERROR_CODES:
            ad_config["urls"], ad_config["start_id"] = create_autoscout24_url(ad_config)
            response = requests.get(ad_config["urls"])

        response.raise_for_status()

        data = response.json()
        ads = data["pageProps"]["listings"]
    except Exception as e:
        logger.error(f"Error while get_ads {url}: {e}")
        send_errors_to_all_chats(e)
        raise e
    return ads, ad_config


def check_conditions(config: dict, ad: dict):
    car_attributes = {attr["iconName"]: attr["data"] for attr in ad["vehicleDetails"]}

    # check the maximum price of the ad
    if config["max_price"] is not None:
        ad_price = int(ad["tracking"]["price"])
        if ad_price > config["max_price"]:
            return False

    # check the minimum price of the ad
    if config["min_price"] is not None:
        ad_price = int(ad["tracking"]["price"])
        if ad_price < config["min_price"]:
            return False

    # check the minimum production year of the car or if not exists
    if config["min_year"] is not None:
        year = car_attributes.get("calendar")
        if year:
            year = year.split("/")[-1]
        if not year or int(year) < config["min_year"]:
            return False

    # check the maximum production year of the car or if not exists
    if config["max_year"] is not None:
        year = car_attributes.get("calendar")
        if year:
            year = year.split("/")[-1]

        if not year or int(year) > config["max_year"]:
            return False
    # TODO
    return True


def send_ads(config: dict, ads: list):
    try:
        if config["last_id"] is None:
            # config["last_id"] = ads[0]["id"]
            # logger.info(f"Last found add id for '{config['source']}': {config["last_id"]}")
            # return
            config["last_id"] = ads[1]["id"]

        sorted_ads = []
        for idx, ad in enumerate(ads):
            if ad["id"] == config["last_id"]:
                config["last_id"] = ads[0]["id"]
                sorted_ads = ads[:idx]
                break
            elif idx == len(ads) - 1:
                logger.warning(f"Could not find last id {config['last_id']} in ads")
                config["last_id"] = ads[0]["id"]
                sorted_ads = []

        filtered_ads = []
        for ad in sorted_ads:
            if check_conditions(config, ad):
                filtered_ads.append(ad)

        if not filtered_ads:
            return

        logger.info(f"Last found add id for '{config['source']}': {config["last_id"]}")

        for ad in filtered_ads:
            message, picture_url, listing_url, otomoto_url = config["function_for_message"](ad, config)
            send_telegram_message(
                bot_token=BOT_TOKEN,
                admin_id=config["chat_id"],
                message=message,
                image_url=picture_url,
                autoscout24_url=listing_url,
                otomoto_url=otomoto_url,
            )

    except Exception as e:
        logger.error(f"Error while send_ads : {e}")
        send_errors_to_all_chats(e)
        raise e


def autoscout24_main(config: dict):
    for ad_config_name in config:
        if "autoscout24" not in ad_config_name:
            continue
        ad_config = config[ad_config_name]
        ads, ad_config = get_ads(ad_config["urls"], ad_config)
        send_ads(ads=ads, config=ad_config)

        if "start_time" not in ad_config:
            ad_config["start_time"] = time.time()
        else:
            time_taken = time.time() - ad_config["start_time"]

            if time_taken < MIN_WAIT_TIME:
                time.sleep(MIN_WAIT_TIME - time_taken)
            logger.info(f"Time taken for {ad_config['source']}: {time.time() - ad_config['start_time']}")

            ad_config["start_time"] = time.time()
