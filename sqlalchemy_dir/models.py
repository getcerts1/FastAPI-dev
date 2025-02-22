from database import Base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql import func
"""
Here we will create the ORM model which will translate into our
database tables and their respective columns

DATABASE TABLE MODEL -- SPECIFYING TABLE AND COLUMNS
"""
class Posts(Base):
    __tablename__ = "posts"
    PID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    rating = Column(Integer, nullable=True)
    time_created = Column(TIMESTAMP, nullable=False, server_default=func.now())


class Users(Base):
    __tablename__ = "users"
    UID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False )
    email = Column(String, nullable=True)
    time_created = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __init__(self, first_name, last_name, email):
        #use class construction to self reference user instance and catch user's name and last name
        self.first_name = first_name
        self.last_name = last_name
        if email: #If the email already exists set the attribute for the User instance to be that
            self.email = email
        else:
            self.email = f"{first_name}.{last_name}@company.com" #Else set it to this
