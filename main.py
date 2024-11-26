import os

import requests
from art import tprint

from config import config
from twodehands import create_twodehands_urls, twodehands_main
from autoscout24 import create_autoscout24_url, autoscout24_main
from tools.logger import logger
from tools.utils import validate_config

LIMIT = 100
START_ID = 570


def main():
    response = requests.get("https://httpbin.org/ip")
    tprint("Price Bot")
    logger.info("IP used for the bot is {}".format(response.json()["origin"]))

    pid = os.getpid()
    logger.info(f"Process PID: {pid}")

    for ad_config_name in config:
        ad_config = config[ad_config_name]
        validate_config(ad_config)
        ad_config["last_id"] = None
        if "autoscout24" in ad_config_name:
            ad_config["start_id"] = START_ID
            ad_config["urls"], ad_config["start_id"] = create_autoscout24_url(ad_config)
        elif "2dehands" in ad_config_name:
            ad_config["urls"] = create_twodehands_urls(ad_config)

    while True:
        autoscout24_main()
        twodehands_main()


if __name__ == "__main__":
    main()
