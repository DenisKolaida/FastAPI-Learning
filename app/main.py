# main.py
from fastapi import FastAPI, Response, HTTPException, Header
from typing import Annotated
from app.models import CommonHeaders
from datetime import datetime, date


app = FastAPI()


@app.get("/headers")
async def headers_show(ch: Annotated[CommonHeaders, Header()]):
    return {
        "User-Agent": ch.user_agent,
        "Accept-Language": ch.accept_language
    }


@app.get("/info")
async def headers_show(response: Response, ch: Annotated[CommonHeaders, Header()]):
    response.headers["X-Server-Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": ch.user_agent,
            "Accept-Language": ch.accept_language
        }
    }