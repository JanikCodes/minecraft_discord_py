from sqlalchemy import Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from Classes import WorldHasBlocks
from base import Base


class WorldHasUsers(Base):
    __tablename__ = "world_has_users"

    id = Column("id", Integer, primary_key=True)
    world_id = Column("world_id", Integer, ForeignKey('world.id'))
    user_id = Column("user_id", String(80))
    upper_block_id = Column("upper_block_id", Integer, ForeignKey('world_has_blocks.id'))
    lower_block_id = Column("lower_block_id", Integer, ForeignKey('world_has_blocks.id'))

    # define relationships
    world = relationship("World", back_populates="users")

    def __init__(self, world_id, user_id, upper_block_id, lower_block_id):
        self.world_id = world_id
        self.user_id = user_id
        self.upper_block_id = upper_block_id
        self.lower_block_id = lower_block_id

    def get_position(self, session):
        # query WorldHasBlocks for the x and y values of the lower block
        lower_block_position = session.query(WorldHasBlocks.x, WorldHasBlocks.y) \
            .filter(WorldHasBlocks.id == self.lower_block_id) \
            .first()

        return lower_block_position

    def get_direction(self, session):
        # query WorldHasBlocks for facing direction
        lower_block_direction = session.query(WorldHasBlocks.state_direction) \
            .filter(WorldHasBlocks.id == self.lower_block_id) \
            .first()

        # because the query returns us a tuple e.g. "(-1, )" we need to convert it because we only want the raw int value
        lower_block_direction = lower_block_direction[0] if lower_block_direction else None

        return lower_block_direction

    def update_movement(self, session, dir_x, dir_y):
        # update player facing direction & block_state uppon change
        if dir_x != 0:
            # update state_direction in WorldHasBlocks
            update_block_state_direction = update(WorldHasBlocks) \
                .where(WorldHasBlocks.id.in_([self.upper_block_id, self.lower_block_id])) \
                .values({WorldHasBlocks.state_direction: dir_x})
            session.execute(update_block_state_direction)
            session.commit()

        # update player associated blocks
        update_player_blocks = update(WorldHasBlocks) \
            .where(WorldHasBlocks.id.in_([self.upper_block_id, self.lower_block_id])) \
            .values({
            WorldHasBlocks.x: WorldHasBlocks.x + dir_x,
            WorldHasBlocks.y: WorldHasBlocks.y + dir_y
        })
        session.execute(update_player_blocks)
        session.commit()
