import discord
from Classes.user import User
from discord import app_commands
from discord.ext import commands

import db
from Utils.classes import class_selection


class Runes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="runes", description="Display your runes amount")
    async def runes(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                embed = discord.Embed(title=f"{user.get_userName()} rune amount",
                                      description=f"**{user.get_runes()}** runes")

                embed.set_footer(text="You can earn more while defeating enemies or doing /explore")

                await interaction.response.send_message(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Runes(client))
