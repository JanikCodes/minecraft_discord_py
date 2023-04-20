import discord
from discord import app_commands
from discord.ext import commands

class Play(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="play", description="Start the game session!")
    async def play(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=f"Generating world...",
                                  description=f"Please wait a second while the world is generating..")

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Play(client))
