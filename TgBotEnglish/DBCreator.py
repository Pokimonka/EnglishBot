import os
from distutils.command.check import check

import sqlalchemy
from sqlalchemy import delete, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing.suite.test_reflection import users

from model import create_tables, User, WordsPair, UsersWordsPair

os.environ["DB_USER_NAME"] = "postgres"
os.environ["PASSWORD"] = "Alenka33"
os.environ["DB_NAME"] = "translator"

DB_USER_NAME = os.getenv("DB_USER_NAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DSN = f'postgresql://{DB_USER_NAME}:{PASSWORD}@localhost:5432/{DB_NAME}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()





