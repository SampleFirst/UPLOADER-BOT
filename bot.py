import logging
import os
from aiohttp import web
from pyrogram import Client
from config import Config
from plugins import web_server

# Set up logging configurations
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

PORT = 8080

# Create download directory if it doesn't exist
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name=Config.SESSION_NAME,
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )

    async def start(self):
        app = web.Application()
        app.add_routes([web.get("/", web_server)])
        runner = web.AppRunner(app)
        await runner.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(runner, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

# Create and run the bot instance
app = Bot()
app.run()
