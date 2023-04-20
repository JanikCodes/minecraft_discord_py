import discord
from discord import app_commands
from discord.ext import commands
from Classes.world_size import WorldSize
import db


class World(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="world", description="Is used to generate a new world.")
    @app_commands.choices(world_size=[
        app_commands.Choice(name="small", value=1),
        app_commands.Choice(name="medium", value=2),
        app_commands.Choice(name="big", value=3),
    ])
    async def world(self, interaction: discord.Interaction, world_size: app_commands.Choice[int], world_name: str):
        selected_world_size = WorldSize(id=world_size.value)
        selected_world_name = world_name

        db.add_world(idUser=interaction.user.id, world_name=selected_world_name, world_size=selected_world_size)

        embed = discord.Embed(title=f"World Generation",
                              description=f"Successfully generated a **{selected_world_size.get_name()}** world named `{selected_world_name}`!\n"
                                          f"You can now **join your world** by typing `/play`")

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(World(client))
