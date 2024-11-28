import os
import time
import requests
from art import tprint
from copy import deepcopy

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

    config_copy = deepcopy(config)

    for ad_config_name in config_copy:
        ad_config = config_copy[ad_config_name]
        validate_config(ad_config)
        ad_config["last_id"] = None
        if "autoscout24" in ad_config_name:
            ad_config["start_id"] = START_ID
            ad_config["urls"], ad_config["start_id"] = create_autoscout24_url(ad_config)
        elif "2dehands" in ad_config_name:
            ad_config["urls"] = create_twodehands_urls(ad_config)

    while True:
        autoscout24_main(config_copy)
        twodehands_main(config_copy)


def run_with_restart():
    while True:
        try:
            main()
        except Exception as e:
            logger.error(f"Main function crashed: {e}")
            logger.info("Reloading configuration and restarting in 5 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    run_with_restart()
