
from fastapi import FastAPI
import pandas as pd
import json
def API():
    app = FastAPI()

    @app.post("/sendSwiftRisk/{data}")
    async def sendSwiftRisk(data):
        f = open('Risk.txt',)
        f.write(data)
        return {"item_id": data}

    @app.get("/")
    async def root():
        return {"message": "Hello World"}