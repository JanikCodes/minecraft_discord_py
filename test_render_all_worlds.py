# Execute this file to get a full render of all available worlds
# This is useful for production to quickly see all worlds, what they have build etc.
# Can also be useful for debugging worlds & issues

from sqlalchemy.orm import sessionmaker

from classes import World
from database import engine
from utils.render import render_world_full

Session = sessionmaker(bind=engine)
session = Session()

all_worlds = session.query(World).all()

for world in all_worlds:
    render_world_full(world_id=world.id, session=session)