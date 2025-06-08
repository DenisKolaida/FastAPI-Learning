# обновляем код main.py
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

from app.config import load_config
from app.logger import setup_logger
from app.models import User


app = FastAPI()

logger = setup_logger()
config = load_config()
if config.debug:
    app.debug = True
else:
    app.debug = False


@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")


@app.post("/user")
async def user(user: User):
    return {"name": user.name, "age": user.age, "is_adult": user.age >= 18}
