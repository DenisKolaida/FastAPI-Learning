# main.py
from fastapi import FastAPI, Response, Cookie, HTTPException
from itsdangerous import Signer, BadSignature
import app.db_scripts as dbs
from app.models import UserData
from datetime import date, datetime


COOKIE_NAME = "session_token"
SECRET_KEY = 'HelloWorld'
SESSION_LIFETIME = 5 * 60


app = FastAPI()
signer = Signer(SECRET_KEY)


def check_cookie_time(current_time: int, cookie_time: int):
    difference = current_time - cookie_time
    if difference >= SESSION_LIFETIME or difference <= 0:
        return "bad"
    elif difference >= 3*60:
        return "change"
    return "leave"


@app.get("/delck")
async def delete_cookie(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"message": "Cookie has been set!"}


@app.post("/sign-up")
async def sign_up(user_data: UserData):
    msg = await dbs.create_user(user_data.username, user_data.password)
    return {"mesage":msg}


@app.post("/login")
async def login(user_data: UserData, response: Response):
    uuid = await dbs.login_user(user_data.username, user_data.password)
    uuid = uuid[0] + f".{int(datetime.today().timestamp())}"
    if uuid:
        signed = signer.sign(uuid).decode()
        response.set_cookie(key=COOKIE_NAME, value=signed, httponly=True, max_age=SESSION_LIFETIME)
        return {"message": "Logged successfully."}
    return {"message": "Invalid username or password."}


@app.get("/user")
async def user(response: Response, session_token: str | None = Cookie(default=None)):
    try:
        # If data or user_data is None, it raises TypeError
        data = signer.unsign(session_token).decode().split('.')
        uuid = data[0]
        timestamp = int(data[1])
        current_timestamp = int(datetime.today().timestamp())

        match check_cookie_time(current_timestamp, timestamp):
            case "bad":
                None[0] # Causes TypeError (then 401) which is not logging
            case "change":
                response.set_cookie(key=COOKIE_NAME, value=signer.sign(uuid+f".{current_timestamp}").decode(), httponly=True, max_age=SESSION_LIFETIME)
            case "leave":
                ... # It's just doing nothing :)

        user_data = await dbs.find_user_by_uuid(uuid)
        return {"message":{"username": user_data[0][0], "password": user_data[0][1]}}
    except Exception as e:
        if type(e) != TypeError:
            print(f"[!] ERROR: {e}")
        raise HTTPException(status_code=401)