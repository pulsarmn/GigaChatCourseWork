import aiosqlite
import sqlite3

DB_PATH = "database.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                queries_left INTEGER DEFAULT 20,
                                is_premium INTEGER DEFAULT 0
                            )''')
        await db.commit()


async def add_user(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''',
                         (tg_id,))
        await db.commit()
