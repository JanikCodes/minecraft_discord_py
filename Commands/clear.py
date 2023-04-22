import discord
from discord import app_commands
from discord.ext import commands

import db


class ClearCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="clear", description="Clear all worlds")
    async def clear(self, interaction: discord.Interaction):
        db.delete_all_worlds()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ClearCommand(client))
