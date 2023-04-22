import random

import discord
from discord import app_commands

from Classes.block import Block
from Classes.world_size import WorldSize
from Classes.world import World
from discord.ext import commands
import db

SURFACE_HEIGHT_MAX = 4
TREE_HEIGHT = 3
TREE_CHANCE = 0.20
GRASS_CHANCE = 0.65

class WorldCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="world", description="Is used to generate a new world.")
    @app_commands.choices(world_size=[
        app_commands.Choice(name="small", value=1),
        app_commands.Choice(name="medium", value=2),
        app_commands.Choice(name="big", value=3),
    ])
    async def world(self, interaction: discord.Interaction, world_size: app_commands.Choice[int], world_name: str):
        selected_world_size = WorldSize(id=world_size.value)
        selected_world_name = world_name

        idWorld = db.add_world(idUser=interaction.user.id, world_name=selected_world_name, world_size=selected_world_size)
        world = World(id=idWorld)
        random.seed(str(idWorld))  # use world ID as seed

        embed = discord.Embed(title=f"World Generation",
                              description=f"Currently generating a **{selected_world_size.get_name()}** sized world named `{selected_world_name}`...\n"
                                          f"You can try to **join your world** by typing `/play`")

        await interaction.response.defer()

        await interaction.followup.send(embed=embed)


        # generate noise map
        noise_world = []
        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                random.seed(str(idWorld) + str(x) + str(y))  # use world ID, x, and y as seed
                noise_value = random.uniform(-1, 1)
                scaled_value = (noise_value + 1) / 2  # scale to range of 0 to 1
                noise_world.append([scaled_value] * world.get_world_size().get_y())

        print("Generating world..")
        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                surface_level = world.get_world_size().get_y() // 2  # surface at the middle of the map
                noise_value = noise_world[x][y]
                surface_level += int((noise_value - 0.80) * SURFACE_HEIGHT_MAX)  # adjust surface level based on noise value

                if y <= surface_level:  # air
                    db.add_block_to_world(idWorld=idWorld, idBlock=1, x=x, y=y)
                    world.add_block(Block(1), x, y)
                elif y == surface_level + 1:  # grass
                    db.add_block_to_world(idWorld=idWorld, idBlock=2, x=x, y=y)
                    world.add_block(Block(2), x, y)
                elif y <= surface_level + 3:  # dir
                    db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                    world.add_block(Block(3), x, y)
                else:  # stone
                    scaled_value = (noise_world[x][y] + 1) / 2  # scale to range of 0 to 1
                    if scaled_value > 0.25:  # more stone than dirt
                        if random.random() < 0.05:  # 5% chance of placing a coal block
                            db.add_block_to_world(idWorld=idWorld, idBlock=8, x=x, y=y)  # coal block
                            world.add_block(Block(8), x, y)
                        else:
                            db.add_block_to_world(idWorld=idWorld, idBlock=4, x=x, y=y)  # stone block
                            world.add_block(Block(4), x, y)
                    else:  # more dirt than stone
                        db.add_block_to_world(idWorld=idWorld, idBlock=3, x=x, y=y)
                        world.add_block(Block(3), x, y)

        # add grass
        print("Generating grass..")
        for block in world.get_blocks():
            if block.get_id() == 2: # if it's grass
                if random.uniform(0, 1) > GRASS_CHANCE:
                    if random.uniform(0, 1) > 0.5:
                        db.add_block_to_world(idWorld=idWorld, idBlock=5, x=block.get_x_pos(), y=block.get_y_pos() - 1)
                        world.add_block(block=Block(5), x=block.get_x_pos(), y=block.get_y_pos() - 1)
                    else:
                        db.add_block_to_world(idWorld=idWorld, idBlock=6, x=block.get_x_pos(), y=block.get_y_pos() - 1)
                        world.add_block(block=Block(6), x=block.get_x_pos(), y=block.get_y_pos() - 1)

        # add trees
        print("Generating trees..")
        for block in world.get_blocks():
            if block.get_id() == 2:  # if it's grass
                if world.get_block(block.get_x_pos() + 1, block.get_y_pos() - 2):
                    idBlock = world.get_block(block.get_x_pos() + 1, block.get_y_pos() - 2).get_id()
                    if idBlock != 1: # is it NOT air?
                        if idBlock != 5:
                            if idBlock != 6:
                                continue
                if world.get_block(block.get_x_pos() - 1, block.get_y_pos() - 2):
                    idBlock = world.get_block(block.get_x_pos() - 1, block.get_y_pos() - 2).get_id()
                    if idBlock != 1: # is it NOT air?
                        if idBlock != 5:
                            if idBlock != 6:
                                continue

                if random.uniform(0, 1) < TREE_CHANCE:
                    # spawn a tree
                    generate_tree(world=world, block=block, height=TREE_HEIGHT)

        # Find valid spawn position
        for block in world.get_blocks():
            if block.get_id() == 2:
                # is first block free?
                if world.get_block(block.get_x_pos(), block.get_y_pos() - 1):
                    if world.get_block(block.get_x_pos(), block.get_y_pos() - 1).get_id() == 1:
                        # is second block also free?
                        if world.get_block(block.get_x_pos(), block.get_y_pos() - 2):
                            if world.get_block(block.get_x_pos(), block.get_y_pos() - 2).get_id() == 1:
                                # found valid spawn position!
                                db.add_user_to_world(idWorld=idWorld, idUser=interaction.user.id,x=block.get_x_pos(), y=block.get_y_pos() - 1)
                                break

        print("Finished generating!")

def generate_tree(world, block, height):
    for i in range(1, height + 1):
        # add log blocks
        world.add_block(block=Block(9), x=block.get_x_pos(), y=block.get_y_pos() - i)

    # add leaves
    world.add_block(block=Block(10), x=block.get_x_pos() - 1, y=block.get_y_pos() - height)
    world.add_block(block=Block(10), x=block.get_x_pos(), y=block.get_y_pos() - height)
    world.add_block(block=Block(10), x=block.get_x_pos() + 1, y=block.get_y_pos() - height)

    world.add_block(block=Block(10), x=block.get_x_pos() - 2, y=block.get_y_pos() - height)
    world.add_block(block=Block(10), x=block.get_x_pos() + 2, y=block.get_y_pos() - height)

    world.add_block(block=Block(10), x=block.get_x_pos() - 1, y=block.get_y_pos() - height - 1)
    world.add_block(block=Block(10), x=block.get_x_pos(), y=block.get_y_pos() - height - 1)
    world.add_block(block=Block(10), x=block.get_x_pos() + 1, y=block.get_y_pos() - height - 1)

    world.add_block(block=Block(10), x=block.get_x_pos() - 2, y=block.get_y_pos() - height - 1)
    world.add_block(block=Block(10), x=block.get_x_pos() + 2, y=block.get_y_pos() - height - 1)

    world.add_block(block=Block(10), x=block.get_x_pos() - 1, y=block.get_y_pos() - height - 2)
    world.add_block(block=Block(10), x=block.get_x_pos(), y=block.get_y_pos() - height - 2)
    world.add_block(block=Block(10), x=block.get_x_pos() + 1, y=block.get_y_pos() - height - 2)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WorldCommand(client))
