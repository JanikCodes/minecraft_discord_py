import random
import discord
from discord import app_commands
from Classes.gen_queue_item import GenQueueItem
from Classes.world_size import WorldSize
from Classes.world import World
from discord.ext import commands
from queue_executor import ExecuteWorldQueueGeneration

class WorldCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = client.database

    @app_commands.command(name="world", description="Is used to generate a new world.")
    @app_commands.choices(world_size=[
        app_commands.Choice(name="small", value=1),
        app_commands.Choice(name="medium", value=2),
        app_commands.Choice(name="big", value=3),
    ])
    async def world(self, interaction: discord.Interaction, world_size: app_commands.Choice[int], world_name: str):
        await interaction.response.defer()

        selected_world_size = WorldSize(id=world_size.value, db=self.db)
        selected_world_name = world_name

        idWorld = self.db.add_world(idUser=interaction.user.id, world_name=selected_world_name,
                               world_size=selected_world_size)
        world = World(id=idWorld, db=self.db)
        random.seed(str(idWorld))  # use world ID as seed

        embed = discord.Embed(title=f"World Generation",
                              description=f"Currently generating a **{selected_world_size.get_name()}** sized world named `{selected_world_name}`...\n"
                                          f"This can take a while...")
        embed.colour = discord.Color.red()

        await interaction.followup.send(embed=embed)

        queue_item = GenQueueItem(world=world, idUser=interaction.user.id)
        ExecuteWorldQueueGeneration.add_to_gen_queue(queue_item)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WorldCommand(client))
