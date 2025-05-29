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

from tools.secrets import CONFIG_TO_USE

LIMIT = 100
SLEEP_TIME = 10
LAST_ID_FILE = "./autoscout_lastid.txt"
DEFAULT_START_ID = 746


def read_last_id(file_path: str, default_start_id: int) -> int:
    """Reads the last used ID from the file or returns the default."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            logger.warning(f"Invalid or missing ID in {file_path}. Using default {default_start_id}.")
    return default_start_id


def write_last_id(last_id: int, file_path: str) -> None:
    """Writes the updated last used ID to the file."""
    try:
        with open(file_path, "w") as f:
            f.write(str(last_id))
    except IOError as e:
        logger.error(f"Failed to write {file_path}: {e}")


def main():
    response = requests.get("https://httpbin.org/ip")
    tprint("Price Bot")
    logger.info("IP used for the bot is {}".format(response.json()["origin"]))

    pid = os.getpid()
    logger.info(f"Process PID: {pid}")

    config_copy = deepcopy(config)
    start_id = read_last_id(LAST_ID_FILE, DEFAULT_START_ID)

    ad_config = config_copy[CONFIG_TO_USE]
    validate_config(ad_config)
    ad_config["last_id"] = None
    if "autoscout24" in CONFIG_TO_USE:
        ad_config["start_id"] = start_id
        ad_config["urls"], ad_config["start_id"] = create_autoscout24_url(ad_config)
        write_last_id(ad_config["start_id"], LAST_ID_FILE)
        while True:
            autoscout24_main(config_copy)

    elif "2dehands" in CONFIG_TO_USE:
        ad_config["urls"] = create_twodehands_urls(ad_config)
        while True:
            twodehands_main(config_copy)


def run_with_restart():
    while True:
        try:
            main()
        except Exception as e:
            logger.error(f"Main function crashed: {e}")
            logger.info("Reloading configuration and restarting in 5 seconds...")
            time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    run_with_restart()
