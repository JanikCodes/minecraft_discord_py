import discord
from discord import app_commands
from discord.ext import commands
import db

class TeleportCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="teleport", description="Teleport to x and y cors")
    async def teleport(self, interaction: discord.Interaction, id_world: str, x: str, y: str):
        db.update_user_position(idUser=interaction.user.id, idWorld=id_world, new_x=x, new_y=y)

        await interaction.response.send_message("Successfully teleported!", ephemeral=True, delete_after=2)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(TeleportCommand(client))
