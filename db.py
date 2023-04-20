import mysql.connector

import config
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

    sql = f"INSERT INTO worlds_has_users VALUE(NULL, {idWorld}, {idUser}, 0, 0);"
    cursor.execute(sql)
    mydb.commit()

    print("Added new world")

def get_world_size(idSize):
    sql = f"SELECT idSize, name, x, y FROM world_sizes where idSize = {idSize};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None

def add_block_to_world(idWorld, idBlock, x, y):
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