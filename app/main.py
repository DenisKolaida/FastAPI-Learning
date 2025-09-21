# main.py
from fastapi import FastAPI, Request, HTTPException, Header
from typing import Annotated
import app.db_scripts as dbs


app = FastAPI()


@app.get("/headers")
async def headers_show(response: Request):
    if "User-Agent" not in response.headers or "Accept-Language" not in response.headers:
        raise HTTPException(status_code=400)
    
    return {
        "User-Agent": response.headers["User-Agent"],
        "Accept-Language": response.headers["Accept-Language"]
    }