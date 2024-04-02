import math
import random
import discord
import numpy as np
from discord import app_commands
from discord.ext import commands
from sqlalchemy import insert
from Classes import WorldHasBlocks, World, WorldHasUsers, Block
from Fixtures.BlockFixture import dirt, stone, coal, iron, gold, diamond, stone_darken, grass, air
from session import session

world_width = 60
world_height = 45

surface_biome_max_y = 10
surface_sin_wave_amount = 4

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

        # add new world to db
        world = World(name=world_name, owner=user_id)
        session.add(world)
        session.commit()
        world_id = world.id

        upper_body_block = WorldHasBlocks(world_id=world_id, block_id=11, x=15, y=14)
        session.add(upper_body_block)
        session.commit()

        lower_body_block = WorldHasBlocks(world_id=world_id, block_id=12, x=15, y=15)
        session.add(lower_body_block)
        session.commit()

        # add new user to db relation
        user = WorldHasUsers(world_id=world_id, user_id=user_id, upper_block_id=upper_body_block.id, lower_block_id=lower_body_block.id, x=15, y=15, direction=1)
        session.add(user)
        session.commit()

        embed = discord.Embed(title=f"World Generation",
                              description=f"Currently generating world `{world_name}`...\n"
                                          f"This can take a while...")
        embed.colour = discord.Color.red()

        # start generate process
        generate(world_id)

        await interaction.followup.send(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(GenerateCommand(client))

def generate(world_id):
    blocks = {}
    gen_terrain_base(blocks)
    gen_stone_biome(blocks)
    gen_dirt_biome(blocks)
    gen_ores(blocks)
    gen_caves(blocks)
    gen_surface(blocks)
    persist_blocks(blocks, world_id)

def gen_terrain_base(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y < dirt_biome_max_y:
                blocks[(x, y)] = dirt.id
            else:
                blocks[(x, y)] = stone.id

def gen_stone_biome(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y < dirt_biome_max_y:
                if random.random() < stone_biome_density:
                    paint_in_sphere(blocks, x, y, stone_biome_min_radius, stone_biome_max_radius, stone.id)

def gen_dirt_biome(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y > dirt_biome_max_y:
                if random.random() < dirt_biome_density:
                    paint_in_sphere(blocks, x, y, dirt_biome_min_radius, dirt_biome_max_radius, dirt.id)

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
                blocks[(x, y)] = coal.id
            elif random.random() < iron_chance:
                blocks[(x, y)] = iron.id
            elif random.random() < gold_chance:
                blocks[(x, y)] = gold.id
            elif random.random() < diamond_chance:
                blocks[(x, y)] = diamond.id

def gen_caves(blocks):
    for x in range(world_width):
        for y in range(world_height):
            if y > cave_biome_max_y:
                if random.random() < cave_density:
                    paint_in_sphere(blocks, x, y, cave_min_radius, cave_max_radius, stone_darken.id)

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
        blocks[(x, grass_y)] = grass.id

        # Set blocks above grass to air
        for y in range(0, grass_y):
            blocks[(x, y)] = air.id

def paint_in_sphere(blocks, x, y, min_radius, max_radius, block_id):
    cave_radius = random.uniform(min_radius, max_radius)
    # Mark blocks within the random radius as air.id
    for dx in range(-int(cave_radius), int(cave_radius) + 1):
        for dy in range(-int(cave_radius), int(cave_radius) + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < world_width and 0 <= ny < world_height:
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= cave_radius:
                    blocks[(nx, ny)] = block_id

def persist_blocks(blocks, world_id):
    for (x, y), block_id in blocks.items():
        stmt = insert(WorldHasBlocks).values(world_id=world_id, block_id=block_id, x=x, y=y)
        session.execute(stmt)

    session.commit()
