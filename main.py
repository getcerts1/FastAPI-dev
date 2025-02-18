from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor #provides column name and allows you to map column name to value
import json
from pydantic import BaseModel
from typing import Optional
from Classes import id_check, id_gen
from passwds import PASSWORD

HOST = "localhost"
DATABASE = "firstdatabase"
USER = "postgres"


app = FastAPI()

class PostSchema(BaseModel):
    title:str
    content:str
    rating: Optional[int] = None
    Published: Optional[bool] = True



@app.get("/post/{id}")
async def get_post(id:int):
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor() #This allows you to create the cursor with which to interact with the postgres database
        print("database connection was success")
    except Exception as error:
        print("connection failed")
        print(f"Error: {error}")
