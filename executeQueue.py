import random
import threading
import time
from sqlalchemy.orm import sessionmaker
from Classes import World

world_generation_interval = 3

class ExecuteQueue(threading.Thread):
    from database import engine

    Session = sessionmaker(bind=engine)

    world_queue = []

    @classmethod
    def add_to_queue(self, queue_world):
        self.world_queue.append(queue_world)

    def run(self, *args, **kwargs):
        while True:
            time.sleep(world_generation_interval)

            if len(self.world_queue) > 0:
                # create a new session for this request
                session = self.Session()

                try:
                    # choose a world to generate
                    print("Generating new world from queue..")
                    queue_item = random.choice(self.world_queue)

                    # add new world to db
                    world = World(name=queue_item.world_name, owner=queue_item.user_id)
                    session.add(world)
                    session.commit()

                    # start generate process
                    from Commands.generate import generate_no_async
                    generate_no_async(session=session, world_id=world.id)

                    world.spawn_player(session=session, user_id=queue_item.user_id)

                    self.world_queue.remove(queue_item)

                    session.commit()
                except Exception as e:
                    # rollback the transaction if an error occurs
                    session.rollback()
                    raise e
                finally:
                    # close the session
                    session.close()