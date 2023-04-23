import discord

import db

RENDER_DISTANCE_X = 10
RENDER_DISTANCE_Y = 6

class User:
    def __init__(self, id, x, y, direction, hand_mode):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.hand_mode = hand_mode

    def get_id(self):
        return int(self.id)

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def get_direction(self):
        return self.direction

    def get_hand_mode(self):
        return self.hand_mode

    def update_user(self, world, db):
        user = db.get_user_in_world(idUser=self.id, idWorld=world.get_id())
        self.x = user.get_x_pos()
        self.y = user.get_y_pos()
        self.direction = user.get_direction()
        self.hand_mode = user.get_hand_mode()

    def get_upper_body_emoji(self, interaction):
        if self.direction == 1:
            return discord.utils.get(interaction.client.get_guild(570999180021989377).emojis, name='p_u_r')
        elif self.direction == -1:
            return discord.utils.get(interaction.client.get_guild(570999180021989377).emojis, name='p_u_l')

    def get_lower_body_emoji(self, interaction):
        return discord.utils.get(interaction.client.get_guild(570999180021989377).emojis, name='p_l_r')
