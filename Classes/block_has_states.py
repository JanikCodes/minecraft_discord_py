from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from base import Base


class BlockHasStates(Base):
    __tablename__ = "block_has_states"

    id = Column("id", Integer, primary_key=True)
    block_id = Column("block_id", Integer, ForeignKey('block.id'))
    sprite = Column("sprite", String(40))
    state_active = Column("state_active", Boolean)
    state_direction = Column("state_direction", Integer)

    # Define relationships
    block = relationship("Block", back_populates="block_states")

    def __init__(self, id, block_id, sprite, state_active, state_direction):
        self.id = id
        self.block_id = block_id
        self.sprite = sprite
        self.state_active = state_active
        self.state_direction = state_direction
