"""
ORM object relational mapper is responsible for communicating
between the fastapi app and the database. This allows us to use an
SDK to use python code for communicating with the database. It
offers cross-database compatibility, relatively simple querying
logic and fast deployment.

"""

"""
Define and build models and tables in python instead of having to create the tables
in Postgres for example. This is done using Classes and entries
through objects.
"""

"""
---- THIS FILE IS RESPONSIBLE FOR HANDLING THE CONNECTION ----
"""

from sqlalchemy import create_engine #create connection string
from sqlalchemy.orm import sessionmaker, declarative_base #establish session for memory and base schema for tables in db
from databaseurl import DATABASE_URL
from sqlalchemy_utils import database_exists, create_database

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging SQL statements
print("Connection successful")

# Create database if it doesn’t exist
if not database_exists(engine.url):
    create_database(engine.url)
    print("Database created successfully!")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


