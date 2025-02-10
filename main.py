import json
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


@app.post("/create_posts")
#return a payload variable which is a dict containing json data
#retrieved from the body of the http header in a post request
def return_message(payload: dict = fastapi.params.Body(...)):
    try:
        file_path = "user_data.json"
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump(payload,file)

            with open(file_path, "r+") as file:
                #output json file must be list and anything to append must be a list
                output = json.load(file)
                if isinstance(output, list):
                    output.append(payload)
                else:
                    output = [payload]
                file.seek(0)  # go to the top
                json.dump(payload, file, indent=4) #dump data
                file.truncate()
    except Exception as  e:
        print(f"error with {e}")
    print(payload)
    return {"completed post"}

#we need to validate what data the user is providing, so we have to provide a schema or
#a structured way to get the information from the user