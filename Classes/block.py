import db


class Block:
    def __init__(self, id):
        res = db.get_block(idBlock=id)
        self.id = res[0]
        self.name = res[1]
        self.block_type = res[2]
        self.solid = res[3]
        self.emoji = res[4]
        self.x = 0
        self.y = 0

    def set_x_pos(self, x):
        self.x = x

    def set_y_pos(self, y):
        self.y = y

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_is_solid(self):
        return True if self.solid == 1 else False

    def get_emoji(self):
        return self.emoji
