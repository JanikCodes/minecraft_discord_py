import db

RENDER_DISTANCE_X = 10
RENDER_DISTANCE_Y = 6

class User:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def get_id(self):
        return int(self.id)

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def update_user(self, world):
        user = db.get_user_in_world(idUser=self.id, idWorld=world.get_id())
        self.x = user.get_x_pos()
        self.y = user.get_y_pos()
