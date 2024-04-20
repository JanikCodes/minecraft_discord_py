import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import base

load_dotenv()

# Import all classes
from classes import Block, World, WorldHasBlocks, WorldHasUsers

# Create database structure
host = os.getenv("host")
user = os.getenv("user")
pwd = os.getenv("password")
database = os.getenv("database")
port = os.getenv("port")
# engine = create_engine(f"mysql+pymysql://{user}:{pwd}@{host}/{database}", isolation_level="READ COMMITTED") # Use for MariaDB
engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}", isolation_level="READ COMMITTED") # Use for MySQL
base.Base.metadata.create_all(engine)

