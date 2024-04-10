import asyncio
import random
import threading
import time

import discord
from sqlalchemy.orm import sessionmaker
from Classes import World
from database import engine

world_generation_interval = 3

class ExecuteQueue(threading.Thread):
    from database import engine

    world_queue = []

    def __init__(self, client):
        super().__init__()
        self.client = client

    @classmethod
    def add_to_queue(self, queue_world):
        self.world_queue.append(queue_world)

    async def notify_user(self, user_id, embed, session):
        # notify user that the world is finished
        user = await self.client.fetch_user(user_id)
        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            pass

    def run(self, *args, **kwargs):
        while True:
            time.sleep(world_generation_interval)

            if len(self.world_queue) > 0:
                # create a new session for this request
                Session = sessionmaker(bind=engine)
                session = Session()

                try:
                    # choose a world to generate
                    print("Generating new world from queue..")
                    queue_item = random.choice(self.world_queue)

                    # add new world to db
                    world = World(name=queue_item.world_name, owner=queue_item.user_id)
                    session.add(world)
                    session.commit()

                    # start generate process
                    from Commands.generate import generate_world
                    generate_world(session=session, world_id=world.id)

                    world.spawn_player(session=session, user_id=queue_item.user_id)

                    self.world_queue.remove(queue_item)

                    session.commit()

                    embed = discord.Embed(title="World Generation",
                                          description="Your world has been generated!\nYou can now use `/play` or `/addPlayer`.",
                                          color=discord.Color.green())

                    asyncio.run_coroutine_threadsafe(self.notify_user(user_id=queue_item.user_id, embed=embed, session=session),
                                                     self.client.loop)
                except Exception as e:
                    # rollback the transaction if an error occurs
                    session.rollback()
                    raise e
                finally:
                    # close the session
                    session.close()