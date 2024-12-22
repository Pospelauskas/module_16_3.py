from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, conint, constr

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


class User(BaseModel):
    username: constr(min_length=5, max_length=20)
    age: conint(ge=18, le=120)


@app.get("/users")
def get_users():
    return users


@app.post("/user/{username}/{age}")
def create_user(username: str, age: int):

    new_user_id = str(max(map(int, users.keys()), default=0) + 1)
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: Annotated[str, Path(description="Enter User ID")], username: str, age: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[str, Path(description="Enter User ID")]):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return f"User {user_id} is deleted"



