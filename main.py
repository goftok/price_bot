import os
import time
import requests
from art import tprint
from copy import deepcopy

from config import config
from twodehands import create_twodehands_urls, twodehands_main
from autoscout24 import create_autoscout24_url, autoscout24_main
from tools.console import console
from tools.utils import validate_config

from tools.secrets import CONFIG_TO_USE

LIMIT = 100
SLEEP_TIME = 10


def main():
    response = requests.get("https://httpbin.org/ip")
    tprint("Price Bot")
    console.print("IP used for the bot is {}".format(response.json()["origin"]))

    if not CONFIG_TO_USE:
        raise EnvironmentError("CONFIG_TO_USE should be defined")

    pid = os.getpid()
    console.print(f"Process PID: {pid}")

    config_copy = deepcopy(config)

    ad_config = config_copy[CONFIG_TO_USE]
    validate_config(ad_config)
    ad_config["last_id"] = None
    ad_config["tracked"] = []

    if "autoscout24" in CONFIG_TO_USE:
        ad_config["urls"] = create_autoscout24_url(ad_config)
        while True:
            autoscout24_main(ad_config)

    elif "2dehands" in CONFIG_TO_USE:
        ad_config["urls"] = create_twodehands_urls(ad_config)
        while True:
            twodehands_main(ad_config)


def run_with_restart():
    while True:
        try:
            main()
        except Exception as e:
            console.print(f"Main function crashed: {e}")
            console.print("Reloading configuration and restarting in 5 seconds...")
            time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    run_with_restart()
