from fastapi import FastAPI

app = FastAPI()


@app.get("/feed")
def feed():
    return {"message": "feeded"}
