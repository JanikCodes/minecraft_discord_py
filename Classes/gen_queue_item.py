import db

class GenQueueItem:
    def __init__(self, world, idUser):
        self.world = world
        self.idUser = idUser

    def get_world(self):
        return self.world

    def get_idUser(self):
        return self.idUser