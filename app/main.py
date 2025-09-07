# main.py
import os

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse

import app.db_scripts as dbs
from app.models import Feedback


app = FastAPI()


# Получение пользователя по параметру пути
@app.get("/users/{username}")
async def get_user(username: str):
    return {"error": "User not found"}


# Получение списка пользователей с ограничением (параметр запроса)
@app.get("/users/")
async def read_users(limit: int = 10):
    return None


@app.post("/feedback")
async def feedback(fb: Feedback, is_premium: bool = False):
    await dbs.create_table()
    await dbs.add_feedback(fb.name, fb.message)
    if is_premium:
        return {f"message": f"Спасибо, {fb.name}! Ваш отзыв сохранён. Ваш отзыв будет рассмотрен в приоритетном порядке."}
    return {f"message": f"Спасибо, {fb.name}! Ваш отзыв сохранён."}
