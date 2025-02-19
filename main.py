from fastapi import FastAPI, HTTPException, status
import psycopg2
from psycopg2.extras import RealDictCursor #provides column name and allows you to map column name to value
from pydantic import BaseModel
from typing import Optional
from Classes import id_check, id_gen
from passwds import PASSWORD
import time

HOST = "localhost"
DATABASE = "firstdatabase"
USER = "postgres"


app = FastAPI() #Create the app instance


#create the schema with which users can request within
class PostSchema(BaseModel):
    title:str
    content:str
    rating: Optional[int] = None


#establish a connection to the database
while True:
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
        print("database connection was success")
        break

    except Exception as connection_error:
        print("Connection failed: Try again")
        print(f"Error: {connection_error}")
        time.sleep(2)


@app.get("/get_post/{id}", status_code=status.HTTP_200_OK)
async def get_post(id:str):
    cursor = conn.cursor() #This allows you to create the cursor with which to interact with the postgres database
    cursor.execute(f'SELECT * FROM posts WHERE \"PID\" = {id} ') #Execute the command you want to do by performing the SQL query
    data = cursor.fetchone() #fetches data in the form of json
    if not data:
        return {"message: post with id does not exist"}

    return data



@app.post("/create_post")
async def create_post(post: PostSchema): #when the client sends the http request the raw data in the body has to follow the schema
    id = id_check(id_gen())
    post_dict = post.model_dump()
    post_dict["PID"] = id
    print((post_dict["PID"]))

    cursor = conn.cursor()

    if post_dict["rating"]:
        try:
            cursor.execute(
                '''
                INSERT INTO posts (title, content, rating, "PID")
                VALUES (%s, %s, %s)
                RETURNING *;
                ''',
                (post_dict["title"], post_dict["content"], post_dict["rating"], post_dict["PID"])
            )
            conn.commit() #commit post to the sql db
            data = cursor.fetchall()
            return {"message":"post created successfully"}, data

        except Exception as error:
            return {f"Error {error}"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        try:
            cursor.execute(
                '''
                INSERT INTO posts (title, content, "PID")
                VALUES (%s, %s, %s)
                RETURNING *;
                ''',
                (post_dict["title"], post_dict["content"], post_dict["PID"])
            )
            conn.commit()
            data = cursor.fetchall()
            return data

        except Exception as error:
            return {f'"message": "There was an error: {error}"'}




@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int):
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            DELETE FROM posts WHERE "PID" = %s RETURNING *;
            ''',
            (id,)
        )

        deleted_post = cursor.fetchone()

        if deleted_post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        conn.commit()
        return ({"message": "Delete successful", "deleted_post_id": id},
                {"data":deleted_post})

    except Exception as error:
        conn.rollback()  # Rollback in case of an error
        return {"error": str(error)}


@app.put("/edit_post/{id}")
async def edit_post(id:str, post:PostSchema):
    cursor = conn.cursor()
    post_dict = post.model_dump()

    if post_dict["rating"]:
        cursor.execute("""
        UPDATE posts SET title = %s, content = %s, rating = %s WHERE "PID" = %s
        RETURNING *
        """, (post_dict["title"], post_dict["content"], post_dict["rating"],
              id))

        conn.commit()

        edited_post = cursor.fetchone()
        if not edited_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")


        return {"Message","successfully edited post"}, edited_post

    else:
        cursor.execute("""
                UPDATE posts SET title = %s, content = %s WHERE "PID" = %s
                RETURNING *
                """, (post_dict["title"], post_dict["content"],
                      id))

        conn.commit()

        edited_post = cursor.fetchone()
        if not edited_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")

        return {"Message", "successfully edited post"}, edited_post