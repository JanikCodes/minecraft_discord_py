from sqlalchemy.orm import sessionmaker
from database import engine

Session = sessionmaker(bind=engine)
session = Session()