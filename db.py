import logging
import os
from models import Link
from typing import Optional, Dict

import aiosqlite

logger = logging.getLogger(__name__)


async def migrate():
    """Apply migrations to the database"""

    logger.info("Migrating database...")
    with open("migrations/schema.sql", "r") as sql_file:
        script = sql_file.read()

    async with _DbConnection() as cursor:
        await cursor.executescript(script)
        logger.info("Database migration complete!")


async def create_link(link : str, links : str) -> Optional[Dict]:
    try:
        async with _DbConnection() as cursor:
            await cursor.execute("INSERT INTO links (link, links) VALUES (?, ?)", (link, links))
            return True
    except Exception as e:
        logger.error(e)
        return False

async def get_all_links() -> Optional[Dict]:
    try:
        async with _DbConnection() as cursor:
            await cursor.execute("SELECT * FROM links")
            return await cursor.fetchall()
    except Exception as e:
        logger.error(e)
        return False

async def get_link(link : str) -> Link:
    try:
        async with _DbConnection() as cursor:
            await cursor.execute("SELECT * FROM links WHERE link = ?", (link,))
            db_link = await cursor.fetchone()
            link = Link()
            link.load_from_db(db_link)
            return link
    except Exception as e:
        logger.error(e)
        return False


class _DbConnection:
    @staticmethod
    def __db_path():
        data_dir = "./data"
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)

        return f"{data_dir}/users.db"

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(_DbConnection.__db_path())
        self.cursor = await self.conn.cursor()
        return self.cursor

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.commit()
        await self.cursor.close()
        await self.conn.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(migrate())
    #print(asyncio.run(create_link("test", "test, test2")))
    print(asyncio.run(get_all_links()))
    print(asyncio.run(get_link("test")))
