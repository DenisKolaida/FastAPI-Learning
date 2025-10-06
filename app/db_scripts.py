import asyncio
import sqlite3
import traceback
from uuid import uuid4

import aiosqlite


db_path = "app/db.db"

TABLE_CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS users(
        username TEXT UNIQUE,
        password TEXT,
        uuid TEXT UNIQUE
    )"""


def connect(func):
    async def wrapper(*args, **kwargs):
        try:
            async with aiosqlite.connect(db_path) as db:
                await db.execute("PRAGMA journal_mode=WAL")
                await db.execute(TABLE_CREATION_QUERY)
                result = await func(db, *args, **kwargs)
                await db.commit()
                return result
        except Exception as e:
            print(f"[!] ERROR: {e}")
            traceback.print_exc()
            return None

    return wrapper


@connect
async def create_user(db: aiosqlite.Connection, username, password):

    cursor = await db.execute("SELECT username FROM users WHERE username = ?", (username,))
    if await cursor.fetchall():
        print("========USER EXISTS========")
        return "User with such username already exists."

    while True:
        try:
            await db.execute("INSERT INTO users(username, password, uuid) VALUES (?, ?, ?)", (username, password, str(uuid4())))
            break
        except sqlite3.IntegrityError as e:
            print("Such uuid already exists. Generating new")
    print("========USER CREATED========")
    return f"User {username} created."
    

@connect
async def find_user_by_username(db: aiosqlite.Connection, username):
    cursor = await db.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    return await cursor.fetchall()


@connect
async def find_user_by_uuid(db: aiosqlite.Connection, uuid):
    cursor = await db.execute("SELECT username, password FROM users WHERE uuid = ?", (uuid,))
    return await cursor.fetchall()