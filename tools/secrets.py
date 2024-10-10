import os
from dotenv import load_dotenv

from tools.utils import send_telegram_message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID1 = os.getenv("CHAT_ID1")
CHAT_ID2 = os.getenv("CHAT_ID2")
# CHAT_ID3 = os.getenv("CHAT_ID3")
CHAT_ID4 = os.getenv("CHAT_ID4")
# CHAT_ID5 = os.getenv("CHAT_ID5")
CHAT_ID6 = os.getenv("CHAT_ID6")


if not BOT_TOKEN or not CHAT_ID1:
    raise Exception("BOT_TOKEN or ADMIN_ID is not set")

if not CHAT_ID2:
    print("WARNING: CHAT_ID2 is not set.")
    CHAT_ID2 = CHAT_ID1

# if not CHAT_ID3:
#     print("WARNING: CHAT_ID3 is not set.")
#     CHAT_ID3 = CHAT_ID1

if not CHAT_ID4:
    print("WARNING: CHAT_ID4 is not set.")
    CHAT_ID4 = CHAT_ID1

# if not CHAT_ID5:
#     print("WARNING: CHAT_ID5 is not set.")
#     CHAT_ID5 = CHAT_ID1

if not CHAT_ID6:
    print("WARNING: CHAT_ID6 is not set.")
    CHAT_ID6 = CHAT_ID1


def send_errors_to_all_chats(e: Exception):
    for chat_id in [CHAT_ID1, CHAT_ID2, CHAT_ID4, CHAT_ID6]:
        send_telegram_message(BOT_TOKEN, chat_id, f"bot error: {e}")
