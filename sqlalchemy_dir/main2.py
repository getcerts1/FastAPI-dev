from database import engine, get_db
from models import Base
from sqlalchemy.orm import Session
import crud
import schemas
from fastapi import FastAPI, HTTPException, Depends, status

app = FastAPI()  # Create FastAPI instance

# Initialize database tables (better done with Alembic in production)
Base.metadata.create_all(bind=engine)

# Dependency to get a database session


""" --- GET ENDPOINTS --- """
@app.get("/sqlalchemy/all_posts")
async def test_post(db: Session = Depends(get_db)):
    """Test database connection by retrieving posts"""
    posts =  crud.test_posts(db)  # Call actual database function
    return {"message": "successful", "len":len(posts), "posts": posts}



@app.get("/sqlalchemy/get_posts_id/{id}", response_model=schemas.PostResponse)
async def get_posts_id(id:int, db: Session = Depends(get_db)):
    post = crud.get_posts_id(db,post_id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return post



@app.get("/sqlalchemy/get_user_id/{id}", response_model=schemas.UserResponse)
async def get_user_id(id:int, db: Session = Depends(get_db)):
    user = crud.get_user_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user







""" --- POST ENDPOINTS --- """
#1) create api endpoint 2) tell fastapi to return response following BaseModel schema 3) set session and
#http request check to follow incoming schema 4) Run crud logic 5) return response
@app.post("/sqlalchemy/add_posts", response_model=schemas.PostResponse)
async def add_post(post: schemas.PostRequest, db: Session = Depends(get_db)):
    new_post = crud.add_new_post(db, post)
    return new_post


@app.post("/sqlalchemy/add_user", response_model=schemas.UserResponse)
async def add_user(user_schema: schemas.UserRequest, db: Session = Depends(get_db)):
    new_user = crud.add_new_user(db, user_schema)
    return new_user








""" --- PUT ENDPOINTS --- """
@app.put("/sqlalchemy/update_post/{id}", response_model=schemas.PostResponse)
async def update_post(id:int, post: schemas.PostRequest, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post, id)
    return updated_post


@app.put("/sqlalchemy/update_user/{id}", response_model=schemas.UserResponse)
async def update_post(id:int, user: schemas.UserRequest, db: Session = Depends(get_db)):
    updated_post = crud.update_user(db,user, id) #provide to the crud function 1)session init 2)user request schema 3) id
    return updated_post









""" --- DELETE ENDPOINTS --- """
@app.delete("/sqlalchemy/delete_post/{id}", response_model=schemas.PostResponse)
async def delete_post(id: int, db:Session = Depends(get_db)):
    deleted_post = crud.delete_post(db,id)
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post to delete")
    return deleted_post


@app.delete("/sqlalchemy/delete_user/{id}", response_model=schemas.UserResponse)
async def delete_post(id: int, db:Session = Depends(get_db)):
    deleted_post = crud.delete_post(db,id)
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user to delete")
    return deleted_post