import aiosqlite
import asyncio
import traceback


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
    await db.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks(
        user_id INTEGER UNIQUE,
        user_name TEXT,
        feedback TEXT
    )""")