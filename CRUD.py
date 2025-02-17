from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from Classes import id_gen, id_check

class PostSchema(BaseModel):
    title: str
    content:str
    rating:Optional[int] = None

FILE_PATH = "user_posts.json"
app = FastAPI()


@app.get("/get_user_info/{id}", status_code=status.HTTP_200_OK)
async def get_info(id:str):
    try:
        with open(FILE_PATH, "r") as file:
            output = json.load(file)
            for post in output:
                if post.get("id") == id:
                    return post
            return {"Message":"Post not found"}
    except FileNotFoundError:
        return {"Message":f"file does not exist"}, status.HTTP_404_NOT_FOUND



@app.post("/post", status_code=status.HTTP_202_ACCEPTED)
async def new_post(post: PostSchema):
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                try:
                    output = json.load(file)
                    if not isinstance(output, list):
                        output = []
                except json.JSONDecodeError:
                  output = []
        else:
            output = []

        post_dict = post.model_dump()
        post_dict["id"] = id_gen()
        post_dict["id"] = id_check(id_gen())


        output.append(post_dict)

        with open(FILE_PATH, "w") as file:
            json.dump(output, file, indent=4)
            return {"message": f'post added with id {post_dict["id"]}'}


    except FileNotFoundError as f:
        with open(FILE_PATH, "w") as file:
            json.dump([post_dict], file, indent=4)
        return {"message": "First post created!", "post": post_dict}




@app.delete("/delete_post/{id}")
async def delete(id:str):
    try:
        with open(FILE_PATH, "r") as file:
            try:
                output = json.load(file)
                if not isinstance(output, list):
                    output = []
            except json.JSONDecodeError:
                output = []
            not_post = [post for post in output if post.get("id") != id]

            if len(output) == len(not_post):
                return {"Message":"Post does not exist for deletion to take"
                                  "place"}


            with open(FILE_PATH, "w") as file:
                json.dump(not_post, file, indent=4)

            return {"Message":"Deleted post successfully"}

    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            "file does not exist")



@app.put("/edit_post/{id}")
async def put(id:str, post: PostSchema):
    try:
        with open(FILE_PATH, "r") as file:
            try:
                output = json.load(file)
                if not isinstance(output, list):
                    output = []
            except json.JSONDecodeError:
                output = []


        post_dict = post.model_dump()
        post_dict["id"] = id
        print(post_dict)
        for index, entry in enumerate(output):
            if entry.get("id") == id:
                output[index] = post_dict



        with open(FILE_PATH, "w") as file:
            json.dump(output, file, indent=4)

        return {"Message":"post updated"}

    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            "This file does not exist")
