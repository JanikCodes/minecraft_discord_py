import random
import threading
import time
from sqlalchemy.orm import sessionmaker
from Classes import World, WorldHasBlocks, Block

world_generation_interval = 3

class ExecuteQueue(threading.Thread):
    from database import engine

    Session = sessionmaker(bind=engine)
    session = Session()

    world_queue = []

    @classmethod
    def add_to_queue(self, queue_world):
        self.world_queue.append(queue_world)

    def run(self, *args, **kwargs):
        while True:
            time.sleep(world_generation_interval)

            if len(self.world_queue) > 0:
                # choose a world to generate
                print("Generating new world from queue..")
                queue_item = random.choice(self.world_queue)

                # add new world to db
                world = World(name=queue_item.world_name, owner=queue_item.user_id)
                self.session.add(world)
                self.session.commit()

                # start generate process
                from Commands.generate import generate_no_async
                generate_no_async(session=self.session, world_id=world.id)

                non_solid_blocks = self.session.query(WorldHasBlocks.x, WorldHasBlocks.y) \
                    .join(Block) \
                    .filter(WorldHasBlocks.world_id == world.id) \
                    .filter(Block.solid == False) \
                    .all()

                print(len(non_solid_blocks))

                world.spawn_player(session=self.session, user_id=queue_item.user_id)

                self.world_queue.remove(queue_item)

                print("Done!")
