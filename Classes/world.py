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

    def get_block(self, x, y):
        for block in self.blocks:
            if block.get_x_pos() == x and block.get_y_pos() == y:
                return block
        return None