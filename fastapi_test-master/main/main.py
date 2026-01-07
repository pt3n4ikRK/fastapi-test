from fastapi import FastAPI
import uvicorn

from main.main_utils.user_model import Person

app = FastAPI()

users = []

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/about")
def about():
    return {"info": "This api created using FastAPI"}


@app.post("/user/")
def create_user(user: Person):
    users.append(user)
    return {"message": "User created", "user": user}


@app.get("/user")
def get_users():
    return users



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)