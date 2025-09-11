# main.py
import os
from typing import List

from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse

import app.db_scripts as dbs
from app.models import Feedback, UserCreate


app = FastAPI()


@app.get("/page")
async def return_html_page():
    return FileResponse("app/static/index.html")


@app.post("/create_user")
async def create_user(user: UserCreate):
    return {
        "message":f"User {user.name} created.",
        "user_data": user
            }