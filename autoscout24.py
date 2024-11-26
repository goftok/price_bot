import sys
import time
import requests
from config import config

from tools.secrets import BOT_TOKEN
from tools.logger import logger
from tools.telegram import send_telegram_message
from tools.secrets import send_errors_to_all_chats

ERROR_CODES = [403]  # 429
MIN_WAIT_TIME = 120  # seconds


def create_autoscout24_url(config: dict) -> str:
    def get_correct_id_url(query_string: str) -> str:
        start_id = config["start_id"]
        for i in range(100):
            url = f"{config['api_link']}/as24-search-funnel_main-{start_id + i}/lst.json?{query_string}"

            response = requests.get(url)
            if response.status_code == 200:
                return url, start_id + i
        return None, None

    query_params = config["query_params"].copy()
    query_string_parts = []
    for key, value in query_params.items():
        if isinstance(value, list):
            for v in value:
                query_string_parts.append(f"{key}[]={str(v)}")
        else:
            query_string_parts.append(f"{key}={str(value)}")

    query_string = "&".join(query_string_parts)

    url, start_id = get_correct_id_url(query_string)
    if url is None or start_id is None:
        raise Exception(f"Could not find correct id for url for {config["source"]}")

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
        sys.exit(1)
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

        logger.info(f"Last found add id for '{config['source']}': {config["last_id"]}")

        for ad in sorted_ads:
            if not check_conditions(config, ad):
                continue
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
        sys.exit(1)


def autoscout24_main():
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


if __name__ == "__main__":
    config["cars_autoscout24_1"]["start_id"] = 560
    create_autoscout24_url(config["cars_autoscout24_1"])
