from Classes.block import Block
from Classes.world_size import WorldSize
import db

class World:
    def __init__(self, id):
        res = db.get_world(idWorld=id)
        self.id = res[0]
        self.owner = res[1]
        self.name = res[2]
        self.world_size = WorldSize(res[3])
        self.blocks = db.get_world_blocks(idWorld=res[0])

    def get_name(self):
        return self.name

    def get_owner_id(self):
        return self.owner

    def get_world_size(self):
        return self.world_size

    def get_id(self):
        return self.id
    def get_blocks(self):
        return self.blocks

    def add_block(self, block, x, y):
        db.add_block_to_world(idWorld=self.id, idBlock=block.get_id(), x=x, y=y)

        exist_block = self.get_block(x,y)
        if exist_block:
            index = self.blocks.index(exist_block)
            self.blocks[index] = block
        else:
            block.set_x_pos(x)
            block.set_y_pos(y)
            self.blocks.append(block)

    def get_block(self, x, y):
        for block in self.blocks:
            if block.get_x_pos() == x and block.get_y_pos() == y:
                return block

        return None