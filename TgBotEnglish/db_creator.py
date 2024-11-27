import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables

os.environ["DB_USER_NAME"] = "postgres"
os.environ["PASSWORD"] = "Alenka33"
os.environ["DB_NAME"] = "translator"

DB_USER_NAME = os.getenv("DB_USER_NAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DSN = f'postgresql://{DB_USER_NAME}:{PASSWORD}@localhost:5432/{DB_NAME}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    create_tables(engine)




