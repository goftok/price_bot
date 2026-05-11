import re
import time
from typing import Optional, Tuple
from urllib.parse import urlencode

from tools.secrets import BOT_TOKEN
from tools.scraper import scraper
from tools.console import console
from tools.telegram import send_telegram_message
from tools.secrets import send_errors_to_all_chats

ERROR_CODES = [403, 404, 500, 502, 504]  # 429
MIN_WAIT_TIME = 7
TIMEOUT = 5
RETRY_TIMES = 2


def extract_autoscout_build_id(html: str) -> str:
    """
    Extracts something like:
    as24-search-funnel_main-20260421104545

    from:
    /assets/as24-search-funnel/_next/static/as24-search-funnel_main-20260421104545/_buildManifest.js
    """
    patterns = [
        r"/assets/as24-search-funnel/_next/static/([^/]+)/_buildManifest\.js",
        r"/assets/as24-search-funnel/_next/static/([^/]+)/_ssgManifest\.js",
        r'"buildId":"([^"]+)"',
        r"/_next/static/([^/]+)/_buildManifest\.js",
    ]

    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)

    raise ValueError("Could not extract AutoScout24 build id from HTML")


def create_autoscout24_url(config: dict) -> str:
    """
    Attempts to construct a valid AutoScout24 URL by iterating over a range of IDs,
    then returns the first URL that responds with status 200.
    Raises an exception if no valid URL is found.
    """
    api_link = config["api_link"]
    ui_link = config["ui_link"]
    query_params = config["query_params"].copy()

    def get_correct_id_url(query_string: str) -> Optional[str]:
        url = f"{ui_link}?{query_string}"
        for attempt in range(RETRY_TIMES):
            time.sleep(MIN_WAIT_TIME)
            response = scraper.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                return extract_autoscout_build_id(response.text)
            elif response.status_code == 404:
                return None
            elif response.status_code == 429:
                print(f"Rate limit exceeded for URL: {url}. Retrying...")
                time.sleep(MIN_WAIT_TIME * (attempt + 1))
                continue
        return None

    def build_query_string(query_params: dict) -> str:
        items = []

        for key, value in query_params.items():
            if isinstance(value, list):
                for v in value:
                    items.append((f"{key}[]", v))
            else:
                items.append((key, value))

        return urlencode(items, doseq=True)

    query_string = build_query_string(query_params)

    # Attempt to find the correct URL
    start_id = get_correct_id_url(query_string)
    if start_id is None:
        source = config["source"]
        raise Exception(f"Could not find correct id for url for {source}")

    url = f"{api_link}/as24-search-funnel_main-{start_id}/lst.json?{query_string}"
    config["urls"] = url

    console.print(f"Found build id for '{config['source']}': {start_id}")
    return url


def get_ads(url: str, ad_config: dict) -> Tuple[list, dict]:
    try:
        response = scraper.get(url, timeout=TIMEOUT)
        if response.status_code in ERROR_CODES:
            ad_config["urls"] = create_autoscout24_url(ad_config)
            response = scraper.get(ad_config["urls"], timeout=TIMEOUT)

        response.raise_for_status()

        data = response.json()
        ads = data["pageProps"]["listings"]
    except Exception as e:
        console.print(f"Error while get_ads {url}: {e}")
        # send_errors_to_all_chats(e)
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

        if not BOT_TOKEN:
            raise Exception("NO BOT_TOKEN check .env")

        sorted_ads = []
        for ad in ads:
            if ad not in config["tracked"]:
                sorted_ads.append(ad)
                config["tracked"].append(ad)

        filtered_ads = []
        for ad in sorted_ads:
            if check_conditions(config, ad):
                filtered_ads.append(ad)

        if not filtered_ads:
            return

        console.print(f"Last found add id for '{config['source']}': {sorted_ads[-1]["id"]}")

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
        console.print(f"Error while send_ads : {e}")
        send_errors_to_all_chats(e)
        raise e


def autoscout24_main(ad_config: dict):
    ads, ad_config = get_ads(ad_config["urls"], ad_config)
    send_ads(ads=ads, config=ad_config)

    if "start_time" not in ad_config:
        ad_config["start_time"] = time.time()
    else:
        time_taken = time.time() - ad_config["start_time"]

        if time_taken < MIN_WAIT_TIME:
            time.sleep(MIN_WAIT_TIME - time_taken)
        console.print(f"Time taken for {ad_config['source']}: {time.time() - ad_config['start_time']}")

        ad_config["start_time"] = time.time()
