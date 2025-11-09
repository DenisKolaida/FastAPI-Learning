# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from app.models import UserDB

import app.db_scripts as dbs


app = FastAPI()
security = HTTPBasic()
ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/register")
async def register(credentials: HTTPBasicCredentials = Depends(security)):
    return {"message": await dbs.create_user(
        UserDB(
            username=credentials.username,
            h_password=ctx.hash(credentials.password)
            )
        )}


async def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user: UserDB | None = await dbs.find_user_by_username(credentials.username)
    print(user)
    print(credentials)
    if not user or ctx.verify(credentials.password, user.h_password) == False:
        print("=====INCORRECT=======")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
            detail="Incorrect credentials"
            )
    return user


@app.get("/login")
async def login(user: UserDB = Depends(auth_user)):
    return {
        "Message": "You got my secret, welcome",
        "User Info": user
            }


@app.get("/logout")
async def logout():
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have successfully logged out",
            headers={"WWW-Authenticate": "Basic"}
        )