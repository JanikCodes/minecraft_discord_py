import random

from sqlalchemy import and_
from classes import WorldHasBlocks, Block
from fixtures.block_fixture import chicken, grass, air


class Chicken():
    # chance that a chicken stands still for a tick
    idle_chance = 0.4
    # chance that a chicken turns around before walking
    turn_chance = 0.25

    def generate(self, x, y, blocks):
        # spawn a chicken on top of the given position, facing direction is stored in the block state
        blocks[(x, y, 1)] = chicken.id

    def find_spawn_positions(self, blocks):
        # every grass block with an empty (air) block above it is a valid spawn position
        return [(x, y - 1) for (x, y, z), block_id in blocks.items()
                if block_id == grass.id and blocks.get((x, y - 1, 1)) == air.id]

    def update(self, world, session):
        # let every chicken of this world wander around a bit
        chickens = session.query(WorldHasBlocks) \
            .filter(WorldHasBlocks.world_id == world.id, WorldHasBlocks.block_id == chicken.id) \
            .all()

        for chicken_block in chickens:
            if random.random() < self.idle_chance:
                continue

            direction = chicken_block.state_direction
            if random.random() < self.turn_chance:
                direction = -direction

            if not self.walk(session, world, chicken_block, direction):
                # path is blocked, look the other way and try again next tick
                direction = -direction

            chicken_block.state_direction = direction

        session.commit()

    def walk(self, session, world, chicken_block, direction):
        x, y = chicken_block.x + direction, chicken_block.y

        # walk straight ahead
        if self.is_free(session, world, x, y):
            chicken_block.x = x
            return True

        # hop up a single block, physics takes care of falling down again
        if self.is_free(session, world, x, y - 1) and self.is_free(session, world, chicken_block.x, y - 1):
            chicken_block.x = x
            chicken_block.y = y - 1
            return True

        return False

    def is_free(self, session, world, x, y):
        from commands.generate import world_width

        # never walk out of the world
        if x < 0 or x >= world_width or y < 0:
            return False

        solid_block = session.query(WorldHasBlocks.id).join(Block).filter(
            and_(
                WorldHasBlocks.world_id == world.id,
                WorldHasBlocks.x == x,
                WorldHasBlocks.y == y,
                Block.solid == True
            )
        ).first()

        return solid_block is None
