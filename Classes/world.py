from Classes.world_size import WorldSize
import db

class World:
    def __init__(self, id):
        res = db.get_world(idWorld=id)
        self.id = res[0]
        self.owner = res[1]
        self.name = res[2]
        self.world_size = WorldSize(res[3])
        # TODO:
        self.blocks = None

    def get_name(self):
        return self.name

    def get_owner_id(self):
        return self.owner

    def get_world_size(self):
        return self.world_size

    def get_id(self):
        return self.id