import logging
import os
import platform
import time

import discord
from colorama import Back, Fore, Style
from discord.ext import commands

import config
import db

MY_GUILD = discord.Object(id=570999180021989377)

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents().all())
    async def setup_hook(self):
        for fileName in os.listdir('./Commands'):
            if fileName.endswith('.py'):
                await self.load_extension(f'Commands.{fileName[:-3]}')

        await self.tree.sync()

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",
                                                        time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f"{prfx} Logged in as {Fore.YELLOW} {self.user.name}")
        print(f"{prfx} Bot ID {Fore.YELLOW} {str(self.user.id)}")
        print(f"{prfx} Discord Version {Fore.YELLOW} {discord.__version__}")
        print(f"{prfx} Python Version {Fore.YELLOW} {str(platform.python_version())}")
        print(f"{prfx} Bot Version 0.1")
        await db.init_database()

        logging.warning("Now logging..")

client = Client()
client.run(config.botConfig["token"])
