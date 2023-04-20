import discord
from discord import app_commands
from discord.ext import commands
import db

from Classes.world import World

class WorldSelect(discord.ui.Select):
    def __init__(self, idUser):
        super().__init__(placeholder="Choose a world..")
        self.idUser = idUser

        for world in db.get_all_worlds_from_user(idUser=idUser):
            self.add_option(label=f"{world.get_name()}", description=f"size: {world.get_world_size().get_name()}", value=f"{world.get_id()}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.idUser:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.title = "Playing.."
        edited_embed.colour = discord.Color.light_embed()

        await interaction.message.edit(embed=edited_embed, view=None)

class WorldSelectionView(discord.ui.View):
    def __init__(self, idUser):
        super().__init__()

        self.add_item(WorldSelect(idUser=idUser))

class Play(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="play", description="Start your minecraft adventure!")
    async def play(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"World Selection",
                              description=f"Please select a world to play on.")

        await interaction.response.send_message(embed=embed, view=WorldSelectionView(idUser=interaction.user.id))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Play(client))
