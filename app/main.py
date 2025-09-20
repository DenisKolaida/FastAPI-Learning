# main.py
from fastapi import FastAPI, Response, Cookie, HTTPException
from itsdangerous import Signer, BadSignature
from uuid import uuid4

import app.db_scripts as dbs
from app.models import UserData


app = FastAPI()
signer = Signer("HelloWorld")


@app.get("/delck")
async def delete_cookie(response: Response):
    response.delete_cookie(key="session_token")
    return {"message": "Cookie has been set!"}


@app.post("/sign-up")
async def sign_up(user_data: UserData):
    msg = await dbs.create_user(user_data.username, user_data.password)
    return {"mesage":msg}


@app.post("/login")
async def login(user_data: UserData, response: Response):
    uuid = await dbs.login_user(user_data.username, user_data.password)
    if uuid:
        signed_uuid = signer.sign(uuid[0]).decode()
        response.set_cookie(key="session_token", value=signed_uuid, httponly=True, max_age=3600)
        return {"message": "Logged successfully."}
    return {"message": "Invalid username or password."}


@app.get("/user")
async def user(session_token: str | None = Cookie(default=None)):
    try:
        uuid = signer.unsign(session_token).decode()
        user_data = await dbs.find_user_by_uuid(uuid)
        if user_data:
            return {"message":{"username": user_data[0][0], "password": user_data[0][1]}}
        else:
            None[0]
    except Exception as e:
        if not type(e) == TypeError:
            print(f"[!] ERROR: {e}")
        raise HTTPException(status_code=401)
    
    