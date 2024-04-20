import os
import logging
import platform
import discord
from discord.ext import commands, tasks
from sqlalchemy.orm import sessionmaker

from Classes import World
from executeQueue import ExecuteQueue

# import required files
import database
import execute_fixtures


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents().default())
        self.world_count = 0

    async def setup_hook(self):
        for fileName in os.listdir('./Commands'):
            if fileName.endswith('.py'):
                extension = f'Commands.{fileName[:-3]}'
                await self.load_extension(extension)

        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Bot ID {str(self.user.id)}")
        print(f"Discord Version {discord.__version__}")
        print(f"Python Version {str(platform.python_version())}")

        logging.warning("Now logging..")

        # get the initial world count on startup
        Session = sessionmaker(bind=database.engine)
        session = Session()
        self.world_count = session.query(World).count()

        self.update_bot_status.start()

        ExecuteQueue(client=self).start()

    @tasks.loop(seconds=60)
    async def update_bot_status(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.world_count} worlds"))

client = Client()
client.run(os.getenv("token"))




