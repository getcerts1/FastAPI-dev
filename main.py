import fastapi.params
from fastapi import FastAPI
from fastapi.params import Body
import os

a_list = [4, 5, 6]
b_list = [5, 6, 7]
c_list = [6, 7, 8]

new_list = []
for a, b, c in zip(a_list, b_list, c_list):
    if a%2 == 0 or  b%2 == 0 or  c%2 == 0:
        new_list.append((a,b,c))


app = FastAPI()

"""specify the api instance, remember APIs are
tasked with handling data requests and responses.
Next specify the method or the request type,
the API can deal with different request types.
Finally the endpoint, where will the api trigger
the response from. Together this is called a decorator.
"""
@app.get("/intro")
async def get_user():
    return {f"'user': 'u'"}

@app.get("/posts")
def get_posts():
    return {"post": "img.jpg"}


@app.post("/createposts")
#return a payload variable which is a dict containing json data
#retrieved from the body of the http header in a post request
def return_message(payload: dict = fastapi.params.Body(...)):
    print(payload)
    return {"message":"post created!"}
