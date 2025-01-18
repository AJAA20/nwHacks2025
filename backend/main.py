from typing import Union
from fastapi import FastAPI

# https://fastapi.tiangolo.com/#example
app = FastAPI() # Creates an instance of FastAPI, assigning it to the variable `app`

@app.get("/")
def read_root():
    return "nwHacks2025"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "hello": q}


