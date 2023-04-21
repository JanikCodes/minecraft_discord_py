import random

import discord
import noise as noise
from discord import app_commands

from Classes.block import Block
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

        air = 0
        grass = 0
        dirt = 0
        stone = 0
        grass_decorations = 0
        coal = 0

        # generate noise map
        noise_world = []
        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                random.seed((idWorld, x, y))  # use world ID, x, and y as seed
                noise_value = random.uniform(-1, 1)
                scaled_value = (noise_value + 1) / 2  # scale to range of 0 to 1
                noise_world.append([scaled_value] * world.get_world_size().get_y())

        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                surface_level = world.get_world_size().get_y() // 2  # surface at the middle of the map
                noise_value = noise_world[x][y]
                surface_level += int((noise_value - 0.5) * 3)  # adjust surface level based on noise value

                if y <= surface_level:  # air
                    db.add_block_to_world(idWorld=idWorld, idBlock=1, x=x, y=y)
                    world.add_block(Block(1), x, y)
                    air+=1
                elif y == surface_level + 1:  # grass
                    db.add_block_to_world(idWorld=idWorld, idBlock=2, x=x, y=y)
                    world.add_block(Block(2), x, y)
                    grass += 1
                elif y <= surface_level + 4:  # dirt
                    db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                    world.add_block(Block(3), x, y)
                    dirt += 1
                else:  # stone
                    scaled_value = (noise_world[x][y] + 1) / 2  # scale to range of 0 to 1
                    if scaled_value > 0.5:  # more stone than dirt
                        if random.random() < 0.05:  # 5% chance of placing a coal block
                            db.add_block_to_world(idWorld=idWorld, idBlock=8, x=x, y=y)  # coal block
                            world.add_block(Block(8), x, y)
                            coal += 1
                        else:
                            db.add_block_to_world(idWorld=idWorld, idBlock=4, x=x, y=y)  # stone block
                            world.add_block(Block(4), x, y)
                            stone += 1
                    else:  # more dirt than stone
                        db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                        world.add_block(Block(3), x, y)
                        dirt += 1

        for block in world.get_blocks():
            if block.get_id() == 2: # if it's grass
                if random.uniform(0, 1) > 0.5:
                    if random.uniform(0, 1) > 0.5:
                        db.add_block_to_world(idWorld=idWorld, idBlock=5, x=block.get_x_pos(), y=block.get_y_pos() - 1)
                    else:
                        db.add_block_to_world(idWorld=idWorld, idBlock=6, x=block.get_x_pos(), y=block.get_y_pos() - 1)
                    grass_decorations+=1

        print(f"Air: {air}, Grass: {grass}, Dirt: {dirt}, Stone: {stone}, Grass_Deco: {grass_decorations}, Coal: {coal}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WorldCommand(client))
