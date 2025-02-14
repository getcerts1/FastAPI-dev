import json

from fastapi import FastAPI


FILE_PATH = "user_posts.json"
app = FastAPI()


@app.get("/get_user_info/{id}")
async def get_info(id:str):
    try:
        with open(FILE_PATH, "r") as file:
            output = json.load(file)
            for post in output:
                if post.get("id") == id:
                    return post
            return {"Message":"Post not found"}
    except FileNotFoundError:
        return {"Message":f"file does not exist"}



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
        return {"Message":f"file does not exist"}