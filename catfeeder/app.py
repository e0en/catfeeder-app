from contextlib import asynccontextmanager
from datetime import datetime, UTC

import aiohttp
import aiosqlite
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/feed")
async def feed():
    async with aiohttp.request("GET", secret.ENDPOINT) as response:
        if response.status == 200:
            await write_log()
            return {}
        else:
            raise HTTPException(status_code=response.status)


@app.get("/log")
async def add_log():
    await write_log()
    return {}


async def write_log():
    now = datetime.now(tz=UTC).isoformat()
    async with aiosqlite.connect(secret.DB_FILE) as db:
        await db.execute("INSERT INTO feeds (time) VALUES (?)", (now,))
        await db.commit()


@app.get("/times")
async def get_times():
    async with aiosqlite.connect(secret.DB_FILE) as db:
        async with db.execute("SELECT time FROM feeds ORDER BY time DESC") as cursor:
            times = await cursor.fetchall()
    return {"feed_times": [t[0] for t in times]}


@app.get("/")
async def main():
    return FileResponse("static/index.html")
