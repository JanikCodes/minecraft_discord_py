from sqlalchemy.orm import sessionmaker
from engine import engine

Session = sessionmaker(bind=engine)
session = Session()