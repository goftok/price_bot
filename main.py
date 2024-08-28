import sys
import time
import json
import requests
from art import tprint
from random import randint

from config import config
from tools.secrets import BOT_TOKEN
from tools.utils import create_urls, send_telegram_message, console
from tools.utils import get_int_from_itemId, validate_config, calculate_driving_distance, NIJMEGEN, LEUVEN
from tools.utils import send_errors_to_all_chats

LIMIT = 100
SLEEP_TIME = 17  # seconds
RETRY_TIME = 60  # seconds
MIN_WAIT_TIME = 120  # seconds
ERROR_CODES = [502]  # 429


def get_ads(urls: list) -> list:
    ads = []
    for url in urls:
        try:
            response = requests.get(url)
            time.sleep(randint(0, SLEEP_TIME))

            # check if error code is 502 and sleep for 10 seconds
            if response.status_code in ERROR_CODES:
                console.print(f"Error {response.status_code} for URL {url}")
                time.sleep(RETRY_TIME)
                response = requests.get(url)

            response.raise_for_status()
            data = response.json()
            ads.extend(data["listings"])

            # check if there is no more ads in api response
            if len(data["listings"]) < LIMIT:
                break

        except Exception as e:
            console.print(f"Error for URL {url}: {e}")
            # send_errors_to_all_chats(e)
            sys.exit(1)
    return ads


def check_conditions(config: dict, ad: dict) -> bool:
    # check if the add is new
    if config["last_id"] is not None:
        ad_id = get_int_from_itemId(ad["itemId"])
        if ad_id <= config["last_id"]:
            return False

    # check the maximum price of the ad
    if config["max_price"] is not None:
        ad_price = int(ad["priceInfo"]["priceCents"] / 100)
        if ad_price > config["max_price"]:
            return False

    # check the minimum price of the ad
    if config["min_price"] is not None:
        ad_price = int(ad["priceInfo"]["priceCents"] / 100)
        if ad_price < config["min_price"]:
            return False

    # check the distance of the ad is within the limit to nijmegen
    if config["max_distance_nijmegen"] is not None:
        ad_lat = ad["location"]["latitude"]
        ad_long = ad["location"]["longitude"]
        distance_nijmegen = int(calculate_driving_distance(NIJMEGEN, (ad_lat, ad_long)))
        if distance_nijmegen <= config["max_distance_nijmegen"]:
            return False

    # check the distance of the ad is within the limit to leuven
    if config["max_distance_leuven"] is not None:
        ad_lat = ad["location"]["latitude"]
        ad_long = ad["location"]["longitude"]
        distance_leuven = int(calculate_driving_distance(LEUVEN, (ad_lat, ad_long)))
        if distance_leuven <= config["max_distance_leuven"]:
            return False

    # check if the model of is allowed (for car)
    if config["allowed_models"] is not None:
        ad_model = ad["vipUrl"].split("/")[3]
        if ad_model not in config["allowed_models"]:
            return False

    if config["not_allowed_models"] is not None:
        ad_model = ad["vipUrl"].split("/")[3]
        if ad_model in config["not_allowed_models"]:
            return False
    return True


def send_ads(ads: list, config: dict) -> None:
    filtered_ads = []
    for idx, ad in enumerate(ads):

        if not check_conditions(config, ad):
            continue

        if config["last_id"]:
            console.print(
                f"Found ad: '{get_int_from_itemId(ad['itemId'])}' for "
                f"'{config['source']}' with index of '{idx}' size: '{len(ads)}'"
            )
            if idx > len(ads) * 0.9:
                send_errors_to_all_chats(f"WARNING for '{config['source']}'! Ad found at '{idx}' size: '{len(ads)}. Increase number of urls to check.")
        filtered_ads.append(ad)

    sorted_ads = sorted(filtered_ads, key=lambda x: get_int_from_itemId(x["itemId"]), reverse=True)

    if not sorted_ads:
        return

    last_found_ad_id = get_int_from_itemId(sorted_ads[0]["itemId"])
    console.print(f"Last found add id for '{config["source"]}': {last_found_ad_id}")

    # don't send the adds from the first iteration
    if config["last_id"] is None:
        config["last_id"] = last_found_ad_id
        return

    config["last_id"] = last_found_ad_id

    # send the adds
    try:
        for car in sorted_ads:
            bot_message = config["function_for_message"](car, config)
            send_telegram_message(BOT_TOKEN, config["chat_id"], bot_message)
    except Exception as e:
        console.log(f"Error fetching data: {e}")
        send_telegram_message(BOT_TOKEN, config["chat_id"], f"Error fetching data. Check logs for more info. {e}")


def main():
    response = requests.get('https://httpbin.org/ip')
    tprint("Price Bot")
    console.print('IP used for the bot is {}'.format(response.json()['origin']))

    for ad_config in config:
        ad_config = config[ad_config]
        validate_config(ad_config)
        ad_config["urls"] = create_urls(config=ad_config, limit=LIMIT)
        ad_config["last_id"] = None

    while True:
        cache_ads = {}
        for ad_config in config:
            ad_config = config[ad_config]
            query_params = json.dumps(ad_config['query_params'], sort_keys=True)
            cache_key = f"{ad_config['api_link']}_{ad_config['url_numbers']}_{query_params}"

            if cache_key in cache_ads:
                ads = cache_ads[cache_key]
            else:
                ads = get_ads(urls=ad_config["urls"])
                cache_ads[cache_key] = ads

            send_ads(ads=ads, config=ad_config)

            if "start_time" not in ad_config:
                ad_config["start_time"] = time.time()
            else:
                time_taken = time.time() - ad_config["start_time"]

                if time_taken < MIN_WAIT_TIME:
                    time.sleep(MIN_WAIT_TIME - time_taken)

                console.print(f"Time taken for {ad_config['source']}: {time.time() - ad_config["start_time"]}")

                ad_config["start_time"] = time.time()


if __name__ == "__main__":
    main()
