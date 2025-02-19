import json
import string, random
FILE_PATH = "user_posts.json"

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





