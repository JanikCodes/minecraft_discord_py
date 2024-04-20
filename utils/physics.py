from sqlalchemy import and_
from classes import WorldHasBlocks, Block


async def handle_physics(world, session):
    # update all blocks that have gravity enabled
    # update y-1 if a non-solid block exists on that position

    # get all blocks that have gravity enabled for this world
    blocks_with_gravity = session.query(WorldHasBlocks).join(Block).filter(
        and_(WorldHasBlocks.world_id == world.id, Block.gravity == True, Block.z == 1)
    ).order_by(WorldHasBlocks.y.desc()).all()

    affected_by_physics = 0

    for block in blocks_with_gravity:
        # get the block below this block
        block_below = session.query(WorldHasBlocks).join(Block).filter(
            and_(
                WorldHasBlocks.world_id == world.id,
                WorldHasBlocks.x == block.x,
                WorldHasBlocks.y == block.y + 1,
                Block.z == 1
            )
        ).first()

        if block_below is None or not block_below.block.solid:
            # move the block down if the block below is non-solid
            block.y += 1
            affected_by_physics += 1

    # print(f"Physics changed {affected_by_physics} block/s")
    # Commit the changes to the database
    session.commit()
