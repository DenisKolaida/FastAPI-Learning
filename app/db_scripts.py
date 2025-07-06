import asyncio
import traceback

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
            print(f"[!] ОШИБКА: {e}")
            traceback.print_exc()
            return None

    return wrapper


@connect
async def create_table(db: aiosqlite.Connection):
    await db.execute(
        """
    CREATE TABLE IF NOT EXISTS feedbacks(
        user_name TEXT UNIQUE,
        message TEXT
    )"""
    )


@connect
async def add_feedback(db: aiosqlite.Connection, username: str, msg: str):
    await db.execute("""INSERT OR REPLACE INTO feedbacks (user_name, message) VALUES (?,?) """, (username, msg))