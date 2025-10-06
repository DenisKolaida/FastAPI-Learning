# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import User

import app.db_scripts as dbs


app = FastAPI()
security = HTTPBasic()


@app.post("/sign-up")
async def sign_up(credentials: HTTPBasicCredentials = Depends(security)):
    return {"message": await dbs.create_user(credentials.username, credentials.password)}


async def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = await dbs.find_user_by_username(credentials.username)
    print(user)
    print(credentials)
    if not user or not user[0][1] == credentials.password:
        print("=====INCORRECT=======")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
            detail="Incorrect credentials"
            )
    return user[0]


@app.get("/login")
async def login(user: User = Depends(auth_user)):
    return {
        "Message": "You got my secret, welcome",
        "User Info": {
            "Username": user[0],
            "Password": user[1]
        }
            }


@app.get("/logout")
async def logout():
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have successfully logged out",
            headers={"WWW-Authenticate": "Basic"}
        )