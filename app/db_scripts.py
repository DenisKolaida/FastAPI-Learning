import asyncio
import sqlite3
import traceback
from uuid import uuid4

import aiosqlite


db_path = "app/db.db"


def connect(func):
    async def wrapper(*args, **kwargs):
        try:
            async with aiosqlite.connect(db_path) as db:
                await db.execute("PRAGMA journal_mode=WAL")
                result = await func(db, *args, **kwargs)
                await db.commit()
                return result
        except Exception as e:
            print(f"[!] ERROR: {e}")
            traceback.print_exc()
            return None

    return wrapper


@connect
async def create_table(db: aiosqlite.Connection):
    await db.execute(
        """
    CREATE TABLE IF NOT EXISTS users(
        user_name TEXT UNIQUE,
        password TEXT,
        uuid TEXT UNIQUE
    )"""
    )
    print("========CHECKED DB========")


@connect
async def create_user(db: aiosqlite.Connection, user_name, password):

    await create_table()

    cursor = await db.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name,))
    if await cursor.fetchall():
        print("========USER EXISTS========")
        return "User with such username already exists."

    while True:
        try:
            await db.execute("INSERT INTO users(user_name, password, uuid) VALUES (?, ?, ?)", (user_name, password, str(uuid4())))
            break
        except sqlite3.IntegrityError as e:
            print("Such uuid already exists. Generating new")
    print("========USER CREATED========")
    return f"User {user_name} created."
    

@connect
async def login_user(db: aiosqlite.Connection, user_name, password):
    await create_table()
    print("========LOGGING========")
    cursor = await db.execute("SELECT uuid FROM users WHERE user_name = ? AND password = ?", (user_name, password))
    uuid = await cursor.fetchone()
    print(uuid)
    return None