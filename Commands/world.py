import random

import discord
from discord import app_commands
from discord.ext import commands
from Classes.world_size import WorldSize
import db
from Utils import utils


class World(commands.Cog):
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

        # generate blocks in the worldsize dimensions ( width = x, height = y )
        noise_values = utils.generate_perlin_noise(selected_world_size.get_x(), selected_world_size.get_y(),
                                             self.scale, octaves=6, persistence=0.5, lacunarity=2.0, seed=self.seed)
        for x in range(selected_world_size.get_x()):
            for y in range(selected_world_size.get_y()):
                idBlock = random.choice([1, 4])

                # add the block to the database
                db.add_block_to_world(idWorld, idBlock, x, y)

        embed = discord.Embed(title=f"World Generation",
                              description=f"Successfully generated a **{selected_world_size.get_name()}** world named `{selected_world_name}`!\n"
                                          f"You can now **join your world** by typing `/play`")

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(World(client))
