from Classes.world_size import WorldSize


class World:
    def __init__(self, id, db):
        res = db.get_world(idWorld=id)
        self.db = db
        self.id = res[0]
        self.owner = res[1]
        self.name = res[2]
        self.world_size = WorldSize(res[3], db)
        self.blocks = db.get_world_blocks(idWorld=res[0])
        self.users = db.get_all_users_in_world(idWorld=res[0])
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

    def add_block(self, block, x, y, db):
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

    def does_user_lower_part_exist_at_pos(self, x, y):
        for user in self.users:
            if user.x == x and user.y == y:
                return user

        return None

    def does_user_upper_part_exist_at_pos(self, x, y):
        for user in self.users:
            if user.x == x and user.y - 1 == y:
                return user

        return None

    def update_world(self):
        res = self.db.get_world(idWorld=self.id)
        self.blocks = self.db.get_world_blocks(idWorld=res[0])
        self.users = self.db.get_all_users_in_world(idWorld=res[0])

    def find_valid_spawn_position(self):
        for block in self.blocks:
            if block.get_id() == 2:
                # is first block free?
                if self.get_block(block.get_x_pos(), block.get_y_pos() - 1):
                    if self.get_block(block.get_x_pos(), block.get_y_pos() - 1).get_id() == 1:
                        # is second block also free?
                        if self.get_block(block.get_x_pos(), block.get_y_pos() - 2):
                            if self.get_block(block.get_x_pos(), block.get_y_pos() - 2).get_id() == 1:
                                # found valid spawn position!
                                return block.get_x_pos(), block.get_y_pos() - 1
        return 0, 0