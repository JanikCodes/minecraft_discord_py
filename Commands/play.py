import discord
from discord import app_commands, ActionRow
from discord.ext import commands
import db

from Classes.world import World

class BreakModeButton(discord.ui.Button):
    def __init__(self, world, user, row):
        super().__init__(label="Break", style=discord.ButtonStyle.danger, row=row, disabled=False)
        self.world = world
        self.user = user
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.get_id():
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        db.update_user_hand_mode(idUser=interaction.user.id, idWorld=self.world.get_id(), new_hand_mode="break")

        await render_world(user=self.user, world=self.world, interaction=interaction)
class BuildModeButton(discord.ui.Button):
    def __init__(self, world, user, row):
        super().__init__(label="Build", style=discord.ButtonStyle.primary, row=row, disabled=False)
        self.world = world
        self.user = user
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.get_id():
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        db.update_user_hand_mode(idUser=interaction.user.id, idWorld=self.world.get_id(), new_hand_mode="build")

        await render_world(user=self.user, world=self.world, interaction=interaction)
class HandButton(discord.ui.Button):
    def __init__(self, hand_mode, world, user, x, y, row):
        super().__init__(style=discord.ButtonStyle.grey, row=row, disabled=False)
        self.user = user
        self.y = y
        self.x = x
        self.hand_mode = hand_mode
        self.world = world

        match hand_mode:
            case 'break':
                self.emoji = "🪓"
            case 'build':
                self.emoji = "🧊"
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.get_id():
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        match self.hand_mode:
            case 'break':
                db.add_block_to_world(idWorld=self.world.get_id(), idBlock=1, x=self.user.get_x_pos() + self.x, y=self.user.get_y_pos() + self.y)
            case 'build':
                db.add_block_to_world(idWorld=self.world.get_id(), idBlock=4, x=self.user.get_x_pos() + self.x, y=self.user.get_y_pos() + self.y)

        await render_world(user=self.user, world=self.world, interaction=interaction)

class MoveButton(discord.ui.Button):
    def __init__(self, label, user, dir_x, dir_y, world, row):
        super().__init__(label=label, style=discord.ButtonStyle.success, row=row)
        self.user = user
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.world = world
    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.user.get_id():
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        # update player facing direction
        if self.dir_x != 0:
            db.update_user_direction(idUser=self.user.get_id(), idWorld=self.world.get_id(), direction=self.dir_x)

        # do we have a block at that location?
        lower_block = self.world.get_block(self.user.get_x_pos() + self.dir_x, self.user.get_y_pos() + self.dir_y)
        if lower_block:
            if not lower_block.get_is_solid():
                upper_block = self.world.get_block(self.user.get_x_pos() + self.dir_x, self.user.get_y_pos() - 1 + self.dir_y)
                if upper_block:
                    if not upper_block.get_is_solid():
                        db.update_user_position(idUser=self.user.get_id(), idWorld=self.world.get_id(), new_x=self.dir_x, new_y=self.dir_y)


        await render_world(user=self.user, world=self.world, interaction=interaction)

class WorldGameView(discord.ui.View):
    def __init__(self, user, world):
        super().__init__()
        #user.update_user(world=world)
        hand_mode = user.get_hand_mode()
        self.add_item(HandButton(hand_mode=hand_mode, user=user, world=world, x=-1, y=-1, row=1)) #top-left
        self.add_item(MoveButton(label="Up", user=user, dir_x=0, dir_y=-1, world=world, row=1))
        self.add_item(HandButton(hand_mode=hand_mode, user=user, world=world, x=1, y=-1, row=1)) #top-right
        self.add_item(BreakModeButton(world=world, user=user, row=1))
        self.add_item(MoveButton(label="Left", user=user, dir_x=-1, dir_y=0, world=world, row=2))
        self.add_item(HandButton(hand_mode=hand_mode, user=user, world=world, x=user.get_direction(), y=0, row=2)) #center
        self.add_item(MoveButton(label="Right", user=user, dir_x=1, dir_y=0, world=world, row=2))
        self.add_item(BuildModeButton(world=world, user=user, row=2))
        self.add_item(HandButton(hand_mode=hand_mode, user=user, world=world, x=-1, y=1, row=3)) #bottom-left
        self.add_item(MoveButton(label="Down", user=user, dir_x=0, dir_y=1, world=world, row=3))
        self.add_item(HandButton(hand_mode=hand_mode, user=user, world=world, x=1, y=1, row=3)) #bottom-right

async def render_world(user, world, interaction):
    world.update_world()
    user.update_user(world=world)

    # define the view range
    view_range_width = 13
    view_range_height = 10

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
            # generate player bodies on top of it with correct facing direction
            lower_body_user = world.does_user_lower_part_exist_at_pos(x, y)
            upper_body_user = world.does_user_upper_part_exist_at_pos(x, y)

            if lower_body_user:
                row += f"{lower_body_user.get_lower_body_emoji(interaction=interaction)}"
            elif upper_body_user:
                row += f"{upper_body_user.get_upper_body_emoji(interaction=interaction)}"
            else:
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

    return await interaction.message.edit(embed=edited_embed, view=WorldGameView(user=user, world=world))
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

        await render_world(user=user, world=world, interaction=interaction)
class WorldSelectionView(discord.ui.View):
    def __init__(self, idUser):
        super().__init__()

        self.add_item(WorldSelect(idUser=idUser))
class PlayCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="play", description="Start your minecraft adventure!")
    async def play(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"World Selection",
                              description=f"Please select a world to play on.")

        # does user have at least one world?
        if db.get_world_count_from_user(idUser=interaction.user.id) == 0:
            embed.colour = discord.Color.red()
            embed.set_footer(text="You don't have any world ready right now! You can create one with /world")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, view=WorldSelectionView(idUser=interaction.user.id))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(PlayCommand(client))
