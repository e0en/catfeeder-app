from contextlib import asynccontextmanager
from datetime import datetime, UTC

import aiohttp
import aiosqlite
from fastapi import FastAPI, HTTPException

from catfeeder import secret


async def create_db():
    async with aiosqlite.connect(secret.DB_FILE) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS feeds (time TEXT)")
        await db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/feed")
async def feed():
    async with aiohttp.request("GET", secret.ENDPOINT) as response:
        if response.status == 200:
            now = datetime.now(tz=UTC).isoformat()
            async with aiosqlite.connect(secret.DB_FILE) as db:
                await db.execute("INSERT INTO feeds (time) VALUES (?)", (now,))
                await db.commit()
            return {}
        else:
            raise HTTPException(status_code=response.status)


@app.get("/times")
async def get_times():
    async with aiosqlite.connect(secret.DB_FILE) as db:
        async with db.execute("SELECT time FROM feeds ORDER BY time DESC") as cursor:
            times = await cursor.fetchall()
    return {"feed_times": [t[0] for t in times]}
