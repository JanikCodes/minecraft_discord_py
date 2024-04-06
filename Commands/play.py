import io
import discord
from discord import app_commands, File
from discord.ext import commands
from sqlalchemy import update

from Classes import World, WorldHasBlocks
from Classes import WorldHasUsers
from Utils.physics import handle_physics
from Utils.render import render_world
from session import Session


class PlayCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="play", description="Start your adventure!")
    async def playCommand(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id

        embed = discord.Embed(title=f"World Selection",
                              description=f"Please select a world to play on.")

        session = Session()
        try:
            # get player worlds
            worlds = session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()
            if not worlds:
                embed.colour = discord.Color.red()
                embed.set_footer(text="You don't have any world ready right now! You can create one with /generate")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(embed=embed, view=WorldSelectionView(user_id=user_id, session=session))

            session.commit()
        except Exception as e:
            # rollback the transaction if an error occurs
            session.rollback()
            raise e
        finally:
            # close the session
            session.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(PlayCommand(client))


class WorldSelectionView(discord.ui.View):
    def __init__(self, user_id, session):
        super().__init__()

        self.add_item(WorldSelect(user_id=user_id, session=session))


class WorldSelect(discord.ui.Select):
    def __init__(self, user_id, session):
        super().__init__(placeholder="Choose a world..")
        self.user_id = user_id
        self.session = session

        # get all user worlds
        worlds = self.session.query(World).join(World.users).filter(WorldHasUsers.user_id == user_id).all()

        for world in worlds:
            self.add_option(label=f"{world.name}", value=f"{world.id}", emoji="🌎")

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.user_id):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        world_id = self.values[0]

        world = self.session.query(World).filter(World.id == world_id).first()

        await HandleTick(world=world, interaction=interaction, session=self.session)


async def handle_rendering(world, interaction, session):
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
                                            view=WorldGameView(user_id=user_id, world=world, session=session))


class WorldGameView(discord.ui.View):
    def __init__(self, user_id, world, session):
        super().__init__()

        world_has_user = session.query(WorldHasUsers) \
            .filter(WorldHasUsers.world_id == world.id) \
            .filter(WorldHasUsers.user_id == user_id).first()

        # get user current mode
        mode = world_has_user.mode

        if mode == 'BUILD' or mode == 'BREAK':
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=-1, dir_y=-1, world=world, row=1,
                                       session=session))
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=0, dir_y=-2, world=world, row=1,
                                       session=session))
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=1, dir_y=-1, world=world, row=1,
                                       session=session))

            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=-1, dir_y=0, world=world, row=2,
                                       session=session))
            self.add_item(NoneButton(emoji='🚫', row=2))
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=1, dir_y=0, world=world, row=2,
                                       session=session))

            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=-1, dir_y=1, world=world, row=3,
                                       session=session))
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=0, dir_y=1, world=world, row=3,
                                       session=session))
            self.add_item(ActionButton(mode=mode, user=world_has_user, dir_x=1, dir_y=1, world=world, row=3,
                                       session=session))
        else:
            self.add_item(MoveButton(emoji="↖", user=world_has_user, dir_x=-1, dir_y=-1, world=world, row=1, session=session))
            self.add_item(MoveButton(emoji="⬆", user=world_has_user, dir_x=0, dir_y=-1, world=world, row=1, session=session))
            self.add_item(MoveButton(emoji="↗", user=world_has_user, dir_x=1, dir_y=-1, world=world, row=1, session=session))

            self.add_item(MoveButton(emoji="⬅", user=world_has_user, dir_x=-1, dir_y=0, world=world, row=2, session=session))
            self.add_item(NoneButton(emoji='🚫', row=2))
            self.add_item(MoveButton(emoji="➡", user=world_has_user, dir_x=1, dir_y=0, world=world, row=2, session=session))

            self.add_item(MoveButton(emoji="↙", user=world_has_user, dir_x=-1, dir_y=1, world=world, row=3, session=session))
            self.add_item(MoveButton(emoji="⬇", user=world_has_user, dir_x=0, dir_y=1, world=world, row=3, session=session))
            self.add_item(MoveButton(emoji="↘", user=world_has_user, dir_x=1, dir_y=1, world=world, row=3, session=session))

        self.add_item(ModeButton(mode="MOVE", emoji="🏃‍♂️", current_mode=mode, user=world_has_user, world=world, row=1, session=session))
        self.add_item(ModeButton(mode="BREAK", emoji="💥", current_mode=mode, user=world_has_user, world=world, row=2, session=session))
        self.add_item(ModeButton(mode="BUILD", emoji="🧱", current_mode=mode, user=world_has_user, world=world, row=3, session=session))

class ModeButton(discord.ui.Button):
    def __init__(self, mode, emoji, current_mode, user, world, row, session):
        super().__init__(emoji=emoji, row=row)
        self.mode = mode
        self.current_mode = current_mode
        self.user = user
        self.world = world
        self.session = session
        # change button color based if the mode is currently selected or not
        self.style = discord.ButtonStyle.success if current_mode == mode else discord.ButtonStyle.primary
        self.disabled = True if mode == 'BUILD' else False

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != (self.user.user_id):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        # update user mode
        update_mode = update(WorldHasUsers) \
            .where(WorldHasUsers.world_id == self.world.id) \
            .where(WorldHasUsers.user_id == self.user.user_id) \
            .values({WorldHasUsers.mode: self.mode})
        self.session.execute(update_mode)
        self.session.commit()

        await HandleTick(world=self.world, interaction=interaction, session=self.session)


class ActionButton(discord.ui.Button):
    def __init__(self, mode, user, dir_x, dir_y, world, row, session):
        super().__init__(style=discord.ButtonStyle.secondary, row=row)
        self.mode = mode
        self.user = user
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.world = world
        self.emoji = "🖐"
        self.session = session

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.user.user_id):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        world_has_block = self.session.query(WorldHasBlocks) \
            .filter(WorldHasBlocks.world_id == self.world.id).first()

        position = self.user.get_position(session=self.session)

        match self.mode:
            case 'BREAK':
                world_has_block.destroy_block_at_position(session=self.session, x=position.x + self.dir_x,
                                                          y=position.y + self.dir_y)
                pass
            case 'BUILD':
                pass

        await HandleTick(world=self.world, interaction=interaction, session=self.session)


class MoveButton(discord.ui.Button):
    def __init__(self, emoji, user, dir_x, dir_y, world, row, session):
        super().__init__(emoji=emoji, style=discord.ButtonStyle.secondary, row=row)
        self.user = user
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.world = world
        self.session = session

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != str(self.user.user_id):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        # update player movement, direction & associated blocks
        self.user.update_movement(session=self.session, dir_x=self.dir_x, dir_y=self.dir_y)

        await HandleTick(world=self.world, interaction=interaction, session=self.session)

class NoneButton(discord.ui.Button):
    def __init__(self, emoji, row):
        super().__init__(emoji=emoji, style=discord.ButtonStyle.secondary, row=row, disabled=True)

async def HandleTick(world, interaction, session):
    # physics
    await handle_physics(world=world, session=session)
    # render
    await handle_rendering(world=world, interaction=interaction, session=session)
