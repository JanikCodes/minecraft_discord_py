import discord
from discord import app_commands
from discord.ext import commands

class InviteView(discord.ui.View):

    def __init__(self):
        super().__init__()

class InviteCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="invite", description="Invite a player to your mini world!")
    async def invite(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=f"Invite @player",
                                  description=f"Please select one of your worlds..")

            await interaction.response.send_message(embed=embed, view=InviteView())
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(InviteCommand(client))
