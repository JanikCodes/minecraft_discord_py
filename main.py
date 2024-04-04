import os
import logging
import platform
import discord
from discord.ext import commands
from sqlalchemy import delete

from Classes import WorldHasUsers, WorldHasBlocks, World
from Commands.generate import generate
from Utils.render import render_world_no_async
from session import session

draw_entire_world_only = False

# import required files
import database
import executeFixtures

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents().all())

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

if draw_entire_world_only:
    delete_stmt_1 = delete(WorldHasUsers)
    session.execute(delete_stmt_1)
    session.commit()

    delete_stmt_2 = delete(WorldHasBlocks)
    session.execute(delete_stmt_2)
    session.commit()

    delete_stmt_3 = delete(World)
    session.execute(delete_stmt_3)
    session.commit()

    world = World(name="DEBUG", owner="DEBUG")
    session.add(world)
    session.commit()
    world_id = world.id

    upper_body_block = WorldHasBlocks(world_id=world_id, block_id=11, x=15, y=14)
    session.add(upper_body_block)
    session.commit()

    lower_body_block = WorldHasBlocks(world_id=world_id, block_id=12, x=15, y=15)
    session.add(lower_body_block)
    session.commit()

    # add new user to db relation
    user = WorldHasUsers(world_id=world_id, user_id="DEBUG", upper_block_id=upper_body_block.id,
                         lower_block_id=lower_body_block.id)
    session.add(user)
    session.commit()

    generate(world_id)
    render_world_no_async(world_id)
else:
    client = Client()
    client.run(os.getenv("token"))




