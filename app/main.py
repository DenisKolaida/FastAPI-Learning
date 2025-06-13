# main.py
import os

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse

import app.db_scripts as dbs
from app.models import Feedback, User


app = FastAPI()


# Получение пользователя по параметру пути
@app.get("/users/{username}")
async def get_user(username: str):
    return {"error": "User not found"}


# Получение списка пользователей с ограничением (параметр запроса)
@app.get("/users/")
async def read_users(limit: int = 10):
    return None


@app.get("/check_db")
async def check_db():
    if not os.path.exists("app/db.db"):
        await dbs.create_table()
        return {"message": "Database was successfully created."}
    return {"message": "Database exists."}


# Добавление нового пользователя (параметр тела запроса)
@app.post("/add_user", response_model=User)
async def add_user(user: User):
    # fake_db.append({"username": user.username, "user_info": user.user_info})
    return user


@app.post("/feedback")
async def feedback(fb: Feedback): ...
