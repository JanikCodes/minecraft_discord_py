import discord
from discord import app_commands
from discord.ext import commands
import db

from Classes.world import World

def render_world():
    pass

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

        selected_idWorld = self.values[0]
        world = World(id=selected_idWorld)

        # get player's current position
        user = db.get_user_in_world(idUser=interaction.user.id, idWorld=selected_idWorld)

        # define the view range
        view_range_width = 15
        view_range_height = 15

        # calculate the starting and ending coordinates of the view range
        start_x = max(0, user.get_x_pos() - view_range_width // 2)
        end_x = min(world.get_world_size().get_x() - 1, user.get_x_pos() + view_range_width // 2)
        start_y = max(0, user.get_y_pos() - view_range_height // 2)
        end_y = min(world.get_world_size().get_y() - 1, user.get_y_pos() + view_range_height // 2)

        # generate the string representation of the blocks
        blocks_str = ""
        for y in range(start_y, end_y + 1):
            row = ""
            for x in range(start_x, end_x + 1):
                block = world.get_block(x, y)
                block_emoji = discord.utils.get(interaction.client.get_guild(570999180021989377).emojis,
                                                   name=block.get_emoji())

                row += f"{block_emoji}"

            blocks_str += row + "\n"

        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.title = ""
        edited_embed.description = blocks_str

        edited_embed.set_footer(text="")
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
