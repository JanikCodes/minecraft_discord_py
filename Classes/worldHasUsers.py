from sqlalchemy import Column, Integer, ForeignKey, String, update, and_
from sqlalchemy.orm import relationship, aliased
from Classes import WorldHasBlocks, Block
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
        def is_block_solid(x, y):
            # create aliases for the tables
            WorldHasBlocksAlias = aliased(WorldHasBlocks)
            BlockAlias = aliased(Block)

            block_query = session.query(BlockAlias.solid, BlockAlias.id) \
                .join(WorldHasBlocksAlias, WorldHasBlocksAlias.block_id == BlockAlias.id) \
                .filter(WorldHasBlocksAlias.world_id == self.world_id, WorldHasBlocksAlias.x == x, WorldHasBlocksAlias.y == y) \
                .all()

            if block_query is None:
                return False

            found_solid = False
            for block_in_query in block_query:
                if block_in_query.solid:
                    found_solid = True
                    break

            return found_solid

        # update player facing direction & block_state upon direction change
        if dir_x != 0:
            # update state_direction in WorldHasBlocks
            update_block_state_direction = update(WorldHasBlocks) \
                .where(WorldHasBlocks.id.in_([self.upper_block_id, self.lower_block_id])) \
                .values({WorldHasBlocks.state_direction: dir_x})
            session.execute(update_block_state_direction)
            session.commit()

        # check for block collisions that are solid
        if not is_block_solid(self.get_position(session).x + dir_x, self.get_position(session).y + dir_y)\
                and not is_block_solid(self.get_position(session).x + dir_x, self.get_position(session).y - 1 + dir_y):

            # update player associated blocks if valid
            update_player_blocks = update(WorldHasBlocks) \
                .where(WorldHasBlocks.id.in_([self.upper_block_id, self.lower_block_id])) \
                .values({
                WorldHasBlocks.x: WorldHasBlocks.x + dir_x,
                WorldHasBlocks.y: WorldHasBlocks.y + dir_y
            })
            session.execute(update_player_blocks)
            session.commit()