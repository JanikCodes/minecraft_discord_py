from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class WorldHasBlocks(Base):
    __tablename__ = "world_has_blocks"

    id = Column("id", Integer, primary_key=True)
    world_id = Column("world_id", Integer, ForeignKey('world.id'))
    block_id = Column("block_id", Integer, ForeignKey('block.id'))
    x = Column("x", Integer)
    y = Column("y", Integer)

    # Define relationships
    world = relationship("World", back_populates="blocks")
    block = relationship("Block", back_populates="worlds")

    def __init__(self, world_id, block_id, x, y):
        self.world_id = world_id
        self.block_id = block_id
        self.x = x
        self.y = y
