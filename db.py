import mysql.connector

import config
from Classes.block import Block
from Classes.user import User
from Classes.world import World
from Classes.world_size import WorldSize

async def init_database():
    global mydb
    # Connect to the database
    mydb = mysql.connector.connect(
        host=config.botConfig["host"],
        user=config.botConfig["user"],
        password=config.botConfig["password"],
        port=config.botConfig["port"],
        database=config.botConfig["database"],
        charset='utf8mb4'
    )

    global cursor
    cursor = mydb.cursor()

    # Check if the connection is alive
    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")

def add_world(idUser, world_name, world_size):
    sql = f"INSERT INTO worlds VALUE(NULL, {idUser}, '{world_name}', {world_size.get_id()});"
    cursor.execute(sql)
    mydb.commit()

    sql = f"SELECT last_insert_id();"
    cursor.execute(sql)
    idWorld = str(cursor.fetchone()).strip("(,)")

    print("Added new world..")
    return idWorld

def get_world_size(idSize):
    sql = f"SELECT idSize, name, x, y FROM world_sizes where idSize = {idSize};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None

def add_block_to_world(idWorld, idBlock, x, y):
    sql = f"SELECT idRel FROM worlds_has_blocks WHERE idWorld = {idWorld} AND x = {x} AND y = {y};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        # update the block
        sql = f"UPDATE worlds_has_blocks SET idBlock = {idBlock} WHERE idWorld = {idWorld} AND x = {x} AND y = {y};"
        cursor.execute(sql)
        mydb.commit()
    else:
        # There doesnt exist a block yet
        sql = f"INSERT INTO worlds_has_blocks VALUE(NULL, {idWorld}, {idBlock}, {x}, {y});"
        cursor.execute(sql)
        mydb.commit()

def get_world(idWorld):
    sql = f"SELECT idWorld, owner, name, idSize FROM worlds WHERE idWorld = {idWorld};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None

def get_all_worlds_from_user(idUser):
    worlds = []
    sql = f"select w.idWorld FROM worlds w, worlds_has_users r WHERE r.idWorld = w.idWorld AND r.idUser = {idUser};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            worlds.append(World(row[0]))

    return worlds

def get_block(idBlock):
    sql = f"SELECT idBlock, name, idType, solid, emoji FROM blocks WHERE idBlock = {idBlock};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None


def get_world_blocks(idWorld):
    blocks = []
    sql = f"SELECT idBlock, x, y FROM worlds_has_blocks WHERE idWorld = {idWorld};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            block = Block(row[0])
            block.set_x_pos(row[1])
            block.set_y_pos(row[2])
            blocks.append(block)

    return blocks


def get_user_in_world(idUser, idWorld):
    sql = f"SELECT idUser, x, y FROM worlds_has_users WHERE idWorld = {idWorld} AND idUser = {idUser};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return User(res[0], res[1], res[2])

    return None


def update_user_position(idUser, idWorld, new_x, new_y):
    if new_x != 0 and new_y != 0:
        sql = f"UPDATE worlds_has_users SET x = x + {new_x} WHERE idUser = {idUser} AND idWorld = {idWorld};"
        cursor.execute(sql)
        mydb.commit()
        sql = f"UPDATE worlds_has_users SET y = y + {new_y} WHERE idUser = {idUser} AND idWorld = {idWorld};"
        cursor.execute(sql)
        mydb.commit()
    elif new_x != 0:
        # Move along X axis
        sql = f"UPDATE worlds_has_users SET x = x + {new_x} WHERE idUser = {idUser} AND idWorld = {idWorld};"
        cursor.execute(sql)
        mydb.commit()
    elif new_y != 0:
        # Move along Y axis
        sql = f"UPDATE worlds_has_users SET y = y + {new_y} WHERE idUser = {idUser} AND idWorld = {idWorld};"
        cursor.execute(sql)
        mydb.commit()


def delete_all_worlds():
    sql = f"DELETE FROM worlds_has_users;"
    cursor.execute(sql)
    mydb.commit()

    sql = f"DELETE FROM worlds_has_blocks;"
    cursor.execute(sql)
    mydb.commit()

    sql = f"DELETE FROM worlds;"
    cursor.execute(sql)
    mydb.commit()


def add_user_to_world(idWorld, idUser, x, y):
    sql = f"INSERT INTO worlds_has_users VALUE(NULL, {idWorld}, {idUser}, {x}, {y});"
    cursor.execute(sql)
    mydb.commit()


def get_all_users_in_world(idWorld):
    users = []
    sql = f"SELECT idUser, x, y FROM worlds_has_users WHERE idWorld = {idWorld};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            users.append(User(row[0], row[1], row[2]))

        return users
    return None