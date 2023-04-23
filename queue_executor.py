import threading
import time
import random
from Classes.block import Block
from db import Database

SURFACE_HEIGHT_MAX = 4
TREE_HEIGHT = 3
TREE_CHANCE = 0.20
GRASS_CHANCE = 0.65

WORLD_GENERATION_INTERVAL = 3

# TODO
# The core issue right now is that I have 2 threads which both use the same mysql connection, therefore resulting in async behavior
# Solution: Make a seperate connection for the second thread and connect with that to the database, this requires a slight rework of my db.py

class ExecuteWorldQueueGeneration(threading.Thread):

    database = Database()

    gen_queue = []
    @classmethod
    def add_to_gen_queue(self, gen_queue_item):
        self.gen_queue.append(gen_queue_item)

    def run(self,*args,**kwargs):
        while True:
            time.sleep(WORLD_GENERATION_INTERVAL)

            if len(self.gen_queue) > 0:
                # choose a world to generate
                print("Generate new world from queue..")
                queue_item = random.choice(self.gen_queue)

                self.generate_world(world=queue_item.get_world(), idUser=queue_item.get_idUser())

                self.gen_queue.remove(queue_item)

                print("Removed item from queue..")


    def generate_world(self, world, idUser):
        # generate noise map
        idWorld = world.get_id()
        noise_world = []
        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                random.seed(str(idWorld) + str(x) + str(y))  # use world ID, x, and y as seed
                noise_value = random.uniform(-1, 1)
                scaled_value = (noise_value + 1) / 2  # scale to range of 0 to 1
                noise_world.append([scaled_value] * world.get_world_size().get_y())

        for x in range(world.get_world_size().get_x()):
            for y in range(world.get_world_size().get_y()):
                surface_level = world.get_world_size().get_y() // 2  # surface at the middle of the map
                noise_value = noise_world[x][y]
                surface_level += int(
                    (noise_value - 0.80) * SURFACE_HEIGHT_MAX)  # adjust surface level based on noise value

                if y <= surface_level:  # air
                    world.add_block(Block(1, db=self.database), x, y, db=self.database)
                elif y == surface_level + 1:  # grass
                    world.add_block(Block(2, db=self.database), x, y, db=self.database)
                elif y <= surface_level + 3:  # dir
                    world.add_block(Block(3, db=self.database), x, y, db=self.database)
                else:  # stone
                    scaled_value = (noise_world[x][y] + 1) / 2  # scale to range of 0 to 1
                    if scaled_value > 0.25:  # more stone than dirt
                        if random.random() < 0.05:  # 5% chance of placing a coal block
                            world.add_block(Block(8, db=self.database), x, y, db=self.database)
                        else:
                            world.add_block(Block(4, db=self.database), x, y, db=self.database)
                    else:  # more dirt than stone
                        world.add_block(Block(3, db=self.database), x, y, db=self.database)

        for block in world.get_blocks():
            if block.get_id() == 2:  # if it's grass
                if random.uniform(0, 1) > GRASS_CHANCE:
                    if random.uniform(0, 1) > 0.5:
                        world.add_block(block=Block(5, db=self.database), x=block.get_x_pos(), y=block.get_y_pos() - 1, db=self.database)
                    else:
                        world.add_block(block=Block(6, db=self.database), x=block.get_x_pos(), y=block.get_y_pos() - 1, db=self.database)

        # add trees
        print("Generating trees..")
        for block in world.get_blocks():
            if block.get_id() == 2:  # if it's grass
                if world.get_block(block.get_x_pos() + 1, block.get_y_pos() - 2):
                    idBlock = world.get_block(block.get_x_pos() + 1, block.get_y_pos() - 2).get_id()
                    if idBlock != 1:  # is it NOT air?
                        if idBlock != 5:
                            if idBlock != 6:
                                continue
                if world.get_block(block.get_x_pos() - 1, block.get_y_pos() - 2):
                    idBlock = world.get_block(block.get_x_pos() - 1, block.get_y_pos() - 2).get_id()
                    if idBlock != 1:  # is it NOT air?
                        if idBlock != 5:
                            if idBlock != 6:
                                continue

                if random.uniform(0, 1) < TREE_CHANCE:
                    # spawn a tree
                    generate_tree(world=world, block=block, height=TREE_HEIGHT, db=self.database)

        spawn_x, spawn_y = world.find_valid_spawn_position()

        self.database.add_user_to_world(idWorld=world.get_id(), idUser=idUser, x=spawn_x, y=spawn_y)
        print("Finished generating!")


def generate_tree(world, block, height, db):
    for i in range(1, height + 1):
        # add log blocks
        world.add_block(block=Block(9, db=db), x=block.get_x_pos(), y=block.get_y_pos() - i, db=db)

    # add leaves
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() - 1, y=block.get_y_pos() - height, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos(), y=block.get_y_pos() - height, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() + 1, y=block.get_y_pos() - height, db=db)

    world.add_block(block=Block(10, db=db), x=block.get_x_pos() - 2, y=block.get_y_pos() - height, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() + 2, y=block.get_y_pos() - height, db=db)

    world.add_block(block=Block(10, db=db), x=block.get_x_pos() - 1, y=block.get_y_pos() - height - 1, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos(), y=block.get_y_pos() - height - 1, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() + 1, y=block.get_y_pos() - height - 1, db=db)

    world.add_block(block=Block(10, db=db), x=block.get_x_pos() - 2, y=block.get_y_pos() - height - 1, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() + 2, y=block.get_y_pos() - height - 1, db=db)

    world.add_block(block=Block(10, db=db), x=block.get_x_pos() - 1, y=block.get_y_pos() - height - 2, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos(), y=block.get_y_pos() - height - 2, db=db)
    world.add_block(block=Block(10, db=db), x=block.get_x_pos() + 1, y=block.get_y_pos() - height - 2, db=db)