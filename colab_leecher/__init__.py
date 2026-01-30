# ⛏️ MiN3R × Colab Station | https://github.com/AdittyaMondal/MiN3R-Colab-Station

import logging
import json
import asyncio
import uvloop

from pyrogram.client import Client

# Read the dictionary from the txt file
with open("/content/MiN3R-Colab-Station/credentials.json", "r") as file:
    credentials = json.loads(file.read())

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]


logging.basicConfig(level=logging.INFO)

# Install uvloop for better async performance
uvloop.install()

# Create and set event loop explicitly for Python 3.10+ compatibility
# This fixes: RuntimeError: There is no current event loop in thread 'MainThread'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
