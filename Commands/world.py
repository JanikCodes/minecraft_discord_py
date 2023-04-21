import random

import discord
import noise as noise
from discord import app_commands
from Classes.world_size import WorldSize
from Classes.world import World
from discord.ext import commands
import db
from Utils import utils
import noise

class WorldCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.scale = 50  # adjust this to control the roughness of the terrain
        self.threshold = 0.1  # adjust this to control the height of the terrain
        self.seed = 4 # adjust this to change the world seed

    @app_commands.command(name="world", description="Is used to generate a new world.")
    @app_commands.choices(world_size=[
        app_commands.Choice(name="small", value=1),
        app_commands.Choice(name="medium", value=2),
        app_commands.Choice(name="big", value=3),
    ])
    async def world(self, interaction: discord.Interaction, world_size: app_commands.Choice[int], world_name: str):
        selected_world_size = WorldSize(id=world_size.value)
        selected_world_name = world_name

        idWorld = db.add_world(idUser=interaction.user.id, world_name=selected_world_name, world_size=selected_world_size)
        world = World(id=idWorld)

        freq = 16.0 / world.get_world_size().get_x()
        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                if y < 5:
                    db.add_block_to_world(idWorld=idWorld, idBlock=1, x=x, y=y)
                elif y < 8:
                    db.add_block_to_world(idWorld=idWorld, idBlock=2, x=x, y=y)
                else:
                    n = noise.pnoise2(x * freq, y * freq, octaves=4)
                    if n > 0.2:
                        db.add_block_to_world(idWorld=idWorld, idBlock=2, x=x, y=y)
                    elif n > -0.2:
                        db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                    else:
                        db.add_block_to_world(idWorld=idWorld, idBlock=4, x=x, y=y)

        embed = discord.Embed(title=f"World Generation",
                              description=f"Successfully generated a **{selected_world_size.get_name()}** world named `{selected_world_name}`!\n"
                                          f"You can now **join your world** by typing `/play`")

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WorldCommand(client))
