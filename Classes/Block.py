from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Block(Base):
    __tablename__ = "block"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(80))
    solid = Column("solid", Boolean)
    gravity = Column("gravity", Boolean, default=False)
    light_level = Column("light_level", Integer, default=0)
    z = Column("z", Integer, default=0)
    debug_color = Column("debug_color", String(20))

    # Define a relationship to WorldHasBlocks
    worlds = relationship("WorldHasBlocks", back_populates="block")
    block_states = relationship("BlockHasStates", back_populates="block")

    def __init__(self, id, name, solid, gravity, light_level, z, debug_color):
        self.id = id
        self.name = name
        self.solid = solid
        self.gravity = gravity
        self.light_level = light_level
        self.z = z
        self.debug_color = debug_color