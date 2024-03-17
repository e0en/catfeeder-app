from fastapi import FastAPI, HTTPException
import aiohttp

from catfeeder import secret

app = FastAPI()


@app.get("/feed")
async def feed():
    async with aiohttp.request("GET", secret.ENDPOINT) as response:
        if response.status == 200:
            # todo: write current time to database
            return {"message": "feeded"}
        else:
            raise HTTPException(status_code=response.status)
