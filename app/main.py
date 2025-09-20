# main.py
from fastapi import FastAPI, Response, Cookie, HTTPException
from uuid import uuid4

import app.db_scripts as dbs
from app.models import UserData


app = FastAPI()


@app.get("/set-cookie")
async def set_cookie(response: Response):
    response.set_cookie(key="user_id", value="12345", httponly=True)
    return {"message": "Cookie has been set!"}


@app.post("/sign-up")
async def sign_up(user_data: UserData):
    msg = await dbs.create_user(user_data.username, user_data.password)
    return {"mesage":msg}


@app.post("/login")
async def login(user_data: UserData, response: Response):
    uuid = await dbs.login_user(user_data.username, user_data.password)
    if uuid:
        response.set_cookie(key="session_token", value=uuid, httponly=True)
        return {"message": "Logged successfully."}
    return {"message": "Invalid username or password."}


@app.get("/user")
async def user(session_token: str | None = Cookie(default=None)):
    if session_token:
        user_data = await dbs.find_user_by_uuid(session_token)
        if user_data:
            return {"message":{"username": user_data[0][0], "password": user_data[0][1]}}
    raise HTTPException(status_code=401)