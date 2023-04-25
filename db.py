import mysql.connector

import config
from Classes.block import Block
from Classes.user import User
from Classes.world import World


class Database():
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=config.botConfig["host"],
            user=config.botConfig["user"],
            password=config.botConfig["password"],
            port=config.botConfig["port"],
            database=config.botConfig["database"],
            charset='utf8mb4'
        )
        self.cursor = self.mydb.cursor()

        # Check if the connection is alive
        if self.mydb.is_connected():
            print("Database connection successful")
        else:
            print("Database connection failed")

    def add_world(self, idUser, world_name, world_size):
        sql = f"INSERT INTO worlds VALUE(NULL, {idUser}, '{world_name}', {world_size.get_id()});"
        self.cursor.execute(sql)
        self.mydb.commit()

        sql = f"SELECT last_insert_id();"
        self.cursor.execute(sql)
        idWorld = str(self.cursor.fetchone()).strip("(,)")

        print("Added new world..")
        return idWorld

    def get_world_size(self, idSize):
        sql = f"SELECT idSize, name, x, y FROM world_sizes where idSize = {idSize};"
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            return res
        else:
            return None

    def add_block_to_world(self, idWorld, idBlock, x, y):
        sql = f"SELECT idRel FROM worlds_has_blocks WHERE idWorld = {idWorld} AND x = {x} AND y = {y};"
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            # update the block
            sql = f"UPDATE worlds_has_blocks SET idBlock = {idBlock} WHERE idWorld = {idWorld} AND x = {x} AND y = {y};"
            self.cursor.execute(sql)
            self.mydb.commit()
        else:
            # There doesn't exist a block yet
            sql = f"INSERT INTO worlds_has_blocks VALUE(NULL, {idWorld}, {idBlock}, {x}, {y});"
            self.cursor.execute(sql)
            self.mydb.commit()

    def get_world(self, idWorld):
        sql = f"SELECT idWorld, owner, name, idSize FROM worlds WHERE idWorld = {idWorld};"
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            return res
        else:
            return None

    def get_all_worlds_from_user(self, idUser, own_worlds_only=False):
        worlds = []
        if own_worlds_only:
            sql = f"select w.idWorld FROM worlds w, worlds_has_users r WHERE r.idWorld = w.idWorld AND r.idUser = {idUser} AND w.owner = {idUser};"
        else:
            sql = f"select w.idWorld FROM worlds w, worlds_has_users r WHERE r.idWorld = w.idWorld AND r.idUser = {idUser};"
        self.cursor.execute(sql)
        res =self.cursor.fetchall()
        if res:
            for row in res:
                worlds.append(World(row[0], self))

        return worlds

    def get_block(self, idBlock):
        sql = f"SELECT idBlock, name, idType, solid, emoji FROM blocks WHERE idBlock = {idBlock};"
        self.cursor.execute(sql)
        res =self.cursor.fetchone()
        if res:
            return res
        else:
            return None


    def get_world_blocks(self, idWorld):
        blocks = []
        sql = f"SELECT idBlock, x, y FROM worlds_has_blocks WHERE idWorld = {idWorld};"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            for row in res:
                block = Block(row[0], self)
                block.set_x_pos(row[1])
                block.set_y_pos(row[2])
                blocks.append(block)

        return blocks


    def get_user_in_world(self, idUser, idWorld):
        sql = f"SELECT idUser, x, y, direction, hand_mode FROM worlds_has_users WHERE idWorld = {idWorld} AND idUser = {idUser};"
        self.cursor.execute(sql)
        res =self.cursor.fetchone()
        if res:
            return User(res[0], res[1], res[2], res[3], res[4])

        return None


    def update_user_position(self, idUser, idWorld, new_x, new_y):
        if new_x != 0 and new_y != 0:
            sql = f"UPDATE worlds_has_users SET x = x + {new_x} WHERE idUser = {idUser} AND idWorld = {idWorld};"
            self.cursor.execute(sql)
            self.mydb.commit()
            sql = f"UPDATE worlds_has_users SET y = y + {new_y} WHERE idUser = {idUser} AND idWorld = {idWorld};"
            self.cursor.execute(sql)
            self.mydb.commit()
        elif new_x != 0:
            # Move along X axis
            sql = f"UPDATE worlds_has_users SET x = x + {new_x} WHERE idUser = {idUser} AND idWorld = {idWorld};"
            self.cursor.execute(sql)
            self.mydb.commit()
        elif new_y != 0:
            # Move along Y axis
            sql = f"UPDATE worlds_has_users SET y = y + {new_y} WHERE idUser = {idUser} AND idWorld = {idWorld};"
            self.cursor.execute(sql)
            self.mydb.commit()


    def delete_all_worlds(self):
        sql = f"DELETE FROM worlds_has_users;"
        self.cursor.execute(sql)
        self.mydb.commit()

        sql = f"DELETE FROM worlds_has_blocks;"
        self.cursor.execute(sql)
        self.mydb.commit()

        sql = f"DELETE FROM worlds;"
        self.cursor.execute(sql)
        self.mydb.commit()


    def add_user_to_world(self, idWorld, idUser, x, y):
        sql = f"INSERT INTO worlds_has_users VALUE(NULL, {idWorld}, {idUser}, {x}, {y}, 1, 'break');"
        self.cursor.execute(sql)
        self.mydb.commit()

    def get_all_users_in_world(self, idWorld):
        users = []
        sql = f"SELECT idUser, x, y, direction, hand_mode FROM worlds_has_users WHERE idWorld = {idWorld};"
        self.cursor.execute(sql)
        res =self.cursor.fetchall()
        if res:
            for row in res:
                users.append(User(row[0], row[1], row[2], row[3], row[4]))

            return users
        return None

    def update_user_direction(self, idUser, idWorld, direction):
        sql = f"SELECT idRel FROM worlds_has_users WHERE idWorld = {idWorld} AND idUser = {idUser}"
        self.cursor.execute(sql)
        res =self.cursor.fetchall()
        if res:
            sql = f"UPDATE worlds_has_users SET direction = {direction} WHERE idWorld = {idWorld} AND idUser = {idUser};"
            self.cursor.execute(sql)
            self.mydb.commit()

    def get_world_count_from_user(self, idUser, own_worlds_only=False):
        if own_worlds_only:
            sql = f"SELECT Count(*) FROM worlds w WHERE w.owner = {idUser};"
        else:
            sql = f"SELECT COUNT(*) FROM worlds w, worlds_has_users r WHERE r.idWorld = w.idWorld AND r.idUser = {idUser};"

        self.cursor.execute(sql)
        number = str(self.cursor.fetchone()).strip("(,)")
        if number:
            return int(number)


    def update_user_hand_mode(self, idUser, idWorld, new_hand_mode):
        sql = f"SELECT idRel FROM worlds_has_users WHERE idWorld = {idWorld} AND idUser = {idUser}"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            sql = f"UPDATE worlds_has_users SET hand_mode = '{new_hand_mode}' WHERE idWorld = {idWorld} AND idUser = {idUser};"
            self.cursor.execute(sql)
            self.mydb.commit()