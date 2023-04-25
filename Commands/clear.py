import discord
from discord import app_commands
from discord.ext import commands


class ClearCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = client.database

    @app_commands.command(name="clear", description="Clear all worlds")
    async def clear(self, interaction: discord.Interaction):
        self.db.delete_all_worlds()

        await interaction.response.send_message("Successfully cleared all worlds!", ephemeral=True, delete_after=2)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ClearCommand(client))
