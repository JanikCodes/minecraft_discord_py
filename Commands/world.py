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

# Define block distribution
GRASS_DISTRIBUTION = 0.2
DIRT_DISTRIBUTION = 0.5
STONE_DISTRIBUTION = 0.3

# Define perlin noise parameters
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

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

        random.seed(idWorld)  # use world ID as seed

        embed = discord.Embed(title=f"World Generation",
                              description=f"Currently generating a **{selected_world_size.get_name()}** sized world named `{selected_world_name}`...\n"
                                          f"You can try to **join your world** by typing `/play`")

        await interaction.response.send_message(embed=embed)

        # generate noise map
        noise_world = []
        for x in range(world.get_world_size().get_x()):
            noise_row = []
            for y in range(world.get_world_size().get_y()):
                noise_value = noise.snoise2(x / 20, y / 20)
                scaled_value = (noise_value + 1) / 2  # scale to range of 0 to 1
                noise_row.append(scaled_value)
            noise_world.append(noise_row)

        surface_level = world.get_world_size().get_y() // 2  # surface at the middle of the map

        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                if y <= surface_level:  # air
                    db.add_block_to_world(idWorld=idWorld, idBlock=1, x=x, y=y)
                elif y == surface_level + 1:  # grass
                    db.add_block_to_world(idWorld=idWorld, idBlock=2, x=x, y=y)
                elif y <= surface_level + 4:  # dirt
                    db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                else:  # stone
                    scaled_value = (noise_world[x][y] + 1) / 2  # scale to range of 0 to 1
                    if scaled_value > 0.5:  # more stone than dirt
                        db.add_block_to_world(idWorld=idWorld, idBlock=4, x=x, y=y)
                    else:  # more dirt than stone
                        db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WorldCommand(client))
