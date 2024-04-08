from sqlalchemy import Column, Integer, ForeignKey, Boolean, update
from sqlalchemy.orm import relationship

from Classes import Block
from base import Base


class WorldHasBlocks(Base):
    __tablename__ = "world_has_blocks"

    id = Column("id", Integer, primary_key=True)
    world_id = Column("world_id", Integer, ForeignKey('world.id'))
    block_id = Column("block_id", Integer, ForeignKey('block.id'))
    x = Column("x", Integer)
    y = Column("y", Integer)

    # states
    state_active = Column("state_active", Boolean, default=0)
    state_direction = Column("state_direction", Integer, default=1)

    # Define relationships
    world = relationship("World", back_populates="blocks")
    block = relationship("Block", back_populates="worlds")

    def __init__(self, world_id, block_id, x, y):
        self.world_id = world_id
        self.block_id = block_id
        self.x = x
        self.y = y

    def destroy_block_at_position(self, session, x, y, z=1):
        # query WorldHasBlocks to get all entities matching the world_id, x, and y
        # this can return multiple entities based due to the z axis not taken into account yet
        world_blocks_at_position = session.query(WorldHasBlocks) \
            .filter(WorldHasBlocks.world_id == self.world_id) \
            .filter(WorldHasBlocks.x == x) \
            .filter(WorldHasBlocks.y == y) \
            .all()

        for world_block in world_blocks_at_position:
            # check if the z value of the block matches the provided z
            if world_block.block.z == z:
                if world_block.block.breakable:
                    # delete the block rel
                    session.delete(world_block)
                    session.commit()
                    break
                else:
                    # block is not breakable
                    break

    def place_block_at_position(self, session, x, y, block_id, z=1):
        # query WorldHasBlocks to get all entities matching the world_id, x, and y
        # this can return multiple entities based due to the z axis not taken into account yet
        world_blocks_at_position = session.query(WorldHasBlocks) \
            .filter(WorldHasBlocks.world_id == self.world_id) \
            .filter(WorldHasBlocks.x == x) \
            .filter(WorldHasBlocks.y == y) \
            .all()

        if not world_blocks_at_position:

            return

        for world_block in world_blocks_at_position:
            # check if the z value of the block matches the provided z
            if world_block.block.z == z:
                return

        # no blocks at the z value have been found
        # this means we can place a block at the z value
        block = WorldHasBlocks(world_id=self.world_id, block_id=block_id, x=x, y=y)
        session.add(block)
        session.commit()

