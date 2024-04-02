from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from base import Base

class World(Base):
    __tablename__ = "world"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(80))
    owner = Column("owner", String(80))
    
    # Define a relationship to WorldHasBlocks
    blocks = relationship("WorldHasBlocks", back_populates="world")
    users = relationship("WorldHasUsers", back_populates="world")

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner