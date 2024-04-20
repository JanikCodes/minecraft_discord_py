import math
import random
import discord
import numpy as np
from discord import app_commands
from discord.ext import commands
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from classes import WorldHasBlocks, World, WorldHasUsers
from classes.structures.tree import Tree
from classes.queue_world import QueueWorld
from fixtures.block_fixture import dirt, stone, coal, iron, gold, diamond, stone_background, grass, air, melon, \
    world_spawn
from database import engine
from executeQueue import ExecuteQueue

world_width = 60
world_height = 45

surface_biome_max_y = 10
surface_sin_wave_amount = 4

tree_chance = 0.15

cave_biome_max_y = 15
cave_density = 0.01
cave_min_radius = 2
cave_max_radius = 4

stone_biome_density = 0.02
stone_biome_min_radius = 2
stone_biome_max_radius = 3

dirt_biome_max_y = 40
dirt_biome_density = 0.01
dirt_biome_min_radius = 3
dirt_biome_max_radius = 5


class GenerateCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="generate", description="Generate a new world.")
    async def generateCommand(self, interaction: discord.Interaction, world_name: str):
        await interaction.response.defer()

        user_id = interaction.user.id

        # TODO: Make a limit to worlds a user can generate, ( max 3 worlds? )
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            exist_in_worlds = session.query(WorldHasUsers)\
                .filter(WorldHasUsers.user_id == user_id).all()

            # has user reached maximum amount of worlds he can be in?
            if len(exist_in_worlds) < 5:
                ExecuteQueue.add_to_queue(QueueWorld(world_name=world_name, user_id=user_id))

                embed = discord.Embed(title=f"World Generation",
                                      description=f"Added world `{world_name}` to the queue...\n"
                                                  f"This can take a while... ( 15-45 seconds )")
                embed.set_footer(text="You'll be notified by me once I'm done if you have DM's enabled!")
                embed.colour = discord.Color.red()

                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title=f"World Generation",
                                      description=f"You've already reached the maximum amount of worlds you can be in!")
                embed.set_footer(text="You can not delete worlds yet, this will come later down the line")
                embed.colour = discord.Color.red()

                await interaction.followup.send(embed=embed)
        except Exception as e:
            # rollback the transaction if an error occurs
            session.rollback()
            raise e
        finally:
            # close the session
            session.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GenerateCommand(client))


def generate_world(session, world_id):
    blocks = {}
    gen_terrain_base(blocks)
    gen_stone_biome(blocks)
    gen_dirt_biome(blocks)
    gen_ores(blocks)
    gen_caves(blocks)
    gen_surface(blocks)
    gen_trees(blocks)
    gen_spawn_block(blocks)
    persist_blocks(session, blocks, world_id)

def gen_terrain_base(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y < dirt_biome_max_y:
                blocks[(x, y, 1)] = dirt.id

                blocks[(x, y, 0)] = stone_background.id
            else:
                blocks[(x, y, 1)] = stone.id

                # place matching background for every stone
                blocks[(x, y, 0)] = stone_background.id


def gen_stone_biome(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y < dirt_biome_max_y:
                if random.random() < stone_biome_density:
                    paint_in_sphere(blocks, x, y, 1, stone_biome_min_radius, stone_biome_max_radius, stone.id)


def gen_dirt_biome(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y > dirt_biome_max_y:
                if random.random() < dirt_biome_density:
                    paint_in_sphere(blocks, x, y, 1, dirt_biome_min_radius, dirt_biome_max_radius, dirt.id)


def gen_ores(blocks):
    coal_prob = np.interp(np.arange(world_height), [0, world_height], [0, 0.035])
    iron_prob = np.interp(np.arange(world_height), [0, world_height], [0, 0.015])
    gold_prob = np.interp(np.arange(world_height), [0, world_height], [0, 0.01])
    diamond_prob = np.interp(np.arange(world_height), [0, world_height], [0, 0.005])

    for x in range(world_width):
        for y in range(world_height):
            # Sample from the probability distributions for each ore type
            coal_chance = coal_prob[y]
            iron_chance = iron_prob[y]
            gold_chance = gold_prob[y]
            diamond_chance = diamond_prob[y]

            # Check if ore should be generated at this block
            if random.random() < coal_chance:
                blocks[(x, y, 1)] = coal.id
            elif random.random() < iron_chance:
                blocks[(x, y, 1)] = iron.id
            elif random.random() < gold_chance:
                blocks[(x, y, 1)] = gold.id
            elif random.random() < diamond_chance:
                blocks[(x, y, 1)] = diamond.id


def gen_caves(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y > cave_biome_max_y:
                if random.random() < cave_density:
                    paint_in_sphere(blocks, x, y, 1, cave_min_radius, cave_max_radius, None)


def gen_surface(blocks):
    frequencies = [random.uniform(0.5, 2) for _ in range(surface_sin_wave_amount)]
    amplitudes = [random.uniform(-1 / f, 1 / f) for f in frequencies]
    offsets = [random.uniform(0, 2 * math.pi) for _ in range(surface_sin_wave_amount)]

    for x in range(world_width):
        wave_height = sum(
            amplitude * math.sin(frequency * (x + offset))
            for amplitude, frequency, offset in zip(amplitudes, frequencies, offsets)
        ) + surface_biome_max_y

        grass_y = round(wave_height)
        blocks[(x, grass_y, 1)] = grass.id


        # Set blocks above grass to air, even background blocks
        for y in range(0, grass_y):
            blocks[(x, y, 1)] = air.id

            # set background blocks to air
            blocks[(x, y, 0)] = air.id

def gen_trees(blocks):
    # based on tree_chance spawn a tree structure on top of a grass block
    grass_positions = []

    # loop through blocks to find grass positions
    for (x, y, z), block_id in blocks.items():
        if block_id == grass.id:
            grass_positions.append((x, y, z))

    for x, y, z in grass_positions:
        if random.random() < tree_chance:
            Tree().generate(x, y - 1, blocks)

def gen_spawn_block(blocks):
    for (x, y, z), block_id in blocks.items():
        # start searching for spawn area at the center
        if x >= world_width / 2:
            if block_id == grass.id:
                # check if 2 blocks above are air
                if (x, y - 1, z) in blocks and blocks[(x, y - 1, z)] == air.id:
                    if (x, y - 2, z) in blocks and blocks[(x, y - 2, z)] == air.id:
                        blocks[(x, y, z)] = world_spawn.id
                        break

def paint_in_sphere(blocks, x, y, z, min_radius, max_radius, block_id):
    cave_radius = random.uniform(min_radius, max_radius)
    # Mark blocks within the random radius as air.id
    for dx in range(-int(cave_radius), int(cave_radius) + 1):
        for dy in range(-int(cave_radius), int(cave_radius) + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < world_width and 0 <= ny < world_height:
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= cave_radius:
                    if block_id is None:
                        # Check if the key exists before deleting it
                        if (nx, ny, z) in blocks:
                            del blocks[(nx, ny, z)]
                    else:
                        blocks[(nx, ny, z)] = block_id


def persist_blocks(session, blocks, world_id):
    for (x, y, z), block_id in blocks.items():
        stmt = insert(WorldHasBlocks).values(world_id=world_id, block_id=block_id, x=x, y=y)
        session.execute(stmt)

    session.commit()