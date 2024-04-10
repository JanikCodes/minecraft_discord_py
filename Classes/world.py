from sqlalchemy import Column, String, Integer
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

    def spawn_player(self, session, user_id):
        from Classes import WorldHasBlocks, WorldHasUsers

        spawn_pos = self.get_valid_spawn_position(session)

        # add player representive blocks
        upper_body_block = WorldHasBlocks(world_id=self.id, block_id=11, x=spawn_pos.x, y=spawn_pos.y)
        session.add(upper_body_block)
        session.commit()

        lower_body_block = WorldHasBlocks(world_id=self.id, block_id=12, x=spawn_pos.x, y=spawn_pos.y + 1)
        session.add(lower_body_block)
        session.commit()

        # add new user to db relation
        user = WorldHasUsers(world_id=self.id, user_id=user_id, upper_block_id=upper_body_block.id,
                             lower_block_id=lower_body_block.id, selected_block_id=13)
        session.add(user)
        session.commit()


    def get_valid_spawn_position(self, session):
        # query all non-solid blocks in the world
        from Classes import WorldHasBlocks, Block

        non_solid_blocks = session.query(WorldHasBlocks.x, WorldHasBlocks.y) \
            .join(Block) \
            .filter(WorldHasBlocks.world_id == self.id) \
            .filter(Block.solid == False) \
            .all()

        for block_rel in non_solid_blocks:
            # check for a block above the current one because the player needs atleast 2 free blocks to spawn
            block_above = session.query(WorldHasBlocks) \
                .filter_by(world_id=self.id, x=block_rel.x, y=block_rel.y + 1) \
                .first()

            if block_above and not block_above.block.solid:
                # found a valid spawn position
                return block_rel

        # no valid spawn position is found
        return None