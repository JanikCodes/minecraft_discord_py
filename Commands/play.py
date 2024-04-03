import io
import discord
from discord import app_commands, File
from discord.ext import commands
from Classes import World
from Classes import WorldHasUsers
from Utils.physics import handle_physics
from Utils.render import render_world
from session import session


class PlayCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="play", description="Start your adventure!")
    async def playCommand(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id

        embed = discord.Embed(title=f"World Selection",
                              description=f"Please select a world to play on.")

        # get player worlds
        worlds = session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()
        if not worlds:
            embed.colour = discord.Color.red()
            embed.set_footer(text="You don't have any world ready right now! You can create one with /generate")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed, view=WorldSelectionView(user_id=user_id))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(PlayCommand(client))


class WorldSelectionView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()

        self.add_item(WorldSelect(user_id=user_id))


class WorldSelect(discord.ui.Select):
    def __init__(self, user_id):
        super().__init__(placeholder="Choose a world..")
        self.user_id = user_id

        # get all user worlds
        worlds = session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()

        for world in worlds:
            self.add_option(label=f"{world.name}", value=f"{world.id}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):
        world_id = self.values[0]

        world = session.query(World).filter(World.id == world_id).first()

        await HandleTick(world=world, interaction=interaction)


async def handle_rendering(world, interaction):
    user_id = interaction.user.id

    world_image = await render_world(world.id, user_id)

    # convert the world_image to bytes
    image_bytes = io.BytesIO()
    world_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    new_embed = discord.Embed(title=f"Playing {world.name}")
    new_embed.set_image(url="attachment://world_map.png")  # Set the embed's image to the new world map

    # attach the in-memory image file to the embed
    file = File(image_bytes, filename="world_map.png")

    await interaction.response.edit_message(embed=new_embed, attachments=[file],
                                            view=WorldGameView(user_id=user_id, world=world))


class WorldGameView(discord.ui.View):
    def __init__(self, user_id, world):
        super().__init__()

        self.add_item(MoveButton(label="Up", user_id=user_id, dir_x=0, dir_y=-3, world=world, row=1, ))
        self.add_item(MoveButton(label="Left", user_id=user_id, dir_x=-1, dir_y=0, world=world, row=2))
        self.add_item(MoveButton(label="Right", user_id=user_id, dir_x=1, dir_y=0, world=world, row=2))
        self.add_item(MoveButton(label="Down", user_id=user_id, dir_x=0, dir_y=1, world=world, row=3))


class MoveButton(discord.ui.Button):
    def __init__(self, label, user_id, dir_x, dir_y, world, row):
        super().__init__(label=label, style=discord.ButtonStyle.success, row=row)
        self.user_id = user_id
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.world = world

    async def callback(self, interaction: discord.Interaction):
        world_has_user = session.query(WorldHasUsers) \
            .filter(WorldHasUsers.world_id == self.world.id) \
            .filter(WorldHasUsers.user_id == self.user_id).first()

        # update player movement, direction & associated blocks
        world_has_user.update_movement(session=session, dir_x=self.dir_x, dir_y=self.dir_y)

        await HandleTick(world=self.world, interaction=interaction)

async def HandleTick(world, interaction):
    # physics
    await handle_physics(world=world)
    # render
    await handle_rendering(world=world, interaction=interaction)