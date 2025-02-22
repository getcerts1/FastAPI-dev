"""
This post is where all your logic handling takes place, querying and manipulating the database tables.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Posts, Users #import table schemas from models
import schemas

""" --- GET REQUESTS ---"""

def test_posts(db: Session):
    output = db.query(Posts).all() #from the database query the Post table and retrieve all
    return output


def get_posts_id(db: Session, post_id: int):
    """Retrieve a post by its ID"""
    try:
        user = db.query(Posts).filter(Posts.PID == post_id).first()
        return user

    except SQLAlchemyError as error:
        # Log the error
        return {f"Database error: {error}"}



def get_user_id(db: Session, user_id: int):
    try:
        return db.query(Users).filter(Users.UID == user_id).first()
    except SQLAlchemyError as error:
        return {"Database error": error}






""" --- POST REQUESTS --- """

def add_new_post(db: Session, post: schemas.PostRequest):
    """Add a new post with a rating"""
    db_post = Posts(title=post.title, content=post.content, rating=post.rating)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def add_new_user(db: Session, user_data: schemas.UserRequest):
    """
   --- db: Session --- → This is the database session. A temporary workspace where we can interact with the
   database before committing changes.


   --- user_data: UserCreate ---  → This is the validated user input (from the Pydantic schema)
    """

    if user_data.email and "@company" not in user_data.email:
        return {"message":"Wrong email syntax"}

    db_user = Users(first_name=user_data.first_name,last_name=user_data.last_name,email=user_data.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


""" --- PUT REQUEST --- """

def update_post(db: Session, post_schema: schemas.PostRequest, post_id:int):
    selected_post = db.query(Posts).filter(Posts.PID == post_id).first() #retrieve selected row

    post_dict = post_schema.model_dump() #take validated user request
    for key, value in post_dict.items(): #itterate through dict and set each attribute in request key to table column
        setattr(selected_post, key, value)

    db.commit()
    db.refresh(selected_post)
    return selected_post


def update_user(db: Session, user_schema: schemas.UserRequest, user_id:int):
    selected_post = db.query(Posts).filter(Users.UID == user_id).first()  # retrieve selected row

    user_dict = user_schema.model_dump()  # take validated user request
    for key, value in user_dict.items():  # iterate through dict and set each attribute in request key to table column
        setattr(selected_post, key, value)

    db.commit()
    db.refresh(selected_post)
    return selected_post


""" --- DELETE REQUESTS --- """

def delete_post(db: Session, post_id:int):
    selected_post = db.query(Posts).filter(Posts.PID == post_id).first()

    db.delete(selected_post)
    db.commit()
    db.refresh(selected_post)
    return selected_post




def delete_user(db: Session, user_id: int):
    selected_user = db.query(Users).filter(Users.UID == user_id).first

    db.delete(selected_user)
    db.commit()
    db.refresh(selected_user)
    return selected_user