import db

class WorldSize:
    def __init__(self, id):
        res = db.get_world_size(idSize=id)
        self.id = res[0]
        self.name = res[1]
        self.x = res[2]
        self.y = res[3]

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y