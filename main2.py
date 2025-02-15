from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional
import json
import os
import string, random
FILE_PATH = "user_posts.json"

class PostSchema(BaseModel):
    title: str
    content:str
    rating:Optional[int] = None

def id_gen():
    chars = string.ascii_letters + string.digits
    length = random.randint(10,12)
    new_chars = [random.choice(chars) for _ in range(length) ]
    random.shuffle(new_chars)
    return "".join(new_chars)

def id_check(id_value):
    with open(FILE_PATH, "r") as file:
        output = json.load(file)
        for post in output:
            if post.get("id") == id_value:
                return id_gen()
    return id_value

app = FastAPI()

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

