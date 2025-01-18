from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request # to get the request context

# https://fastapi.tiangolo.com/#example
app = FastAPI() # Creates an instance of FastAPI, assigning it to the variable `app`

'''
This object manages the template loading and rendering process. By passing
"templates" to the directory argument, we're telling FastAPI that your
HTML files (like login.html) are located in a folder called templates to where
app.py is located
'''
templates = Jinja2Templates(directory="templates") 

@app.get("/")
def read_root():
    return "nwHacks2025"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "hello": q}


