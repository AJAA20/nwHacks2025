from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request # to get the request context

# https://fastapi.tiangolo.com/#example
app = FastAPI() # Creates an instance of FastAPI, assigning it to the variable `app`

'''
This object manages the template loading and rendering process. By passing
"templates" to the directory argument, we're telling FastAPI that the
HTML files (like test.html) are located in a folder called templates to where
app.py is located
'''
templates = Jinja2Templates(directory="templates") 

# decorator that binds read_root to GET request to the root
# when a user accesses http://localhost:8000/, this function is triggered 
# By default, FastAPI returns JSON responses, but since we're rendering an HTML page
# we specify that the response should be of type HTMLResponse.
# This tells FastAPI to send HTML content back to the client, rather than JSON.
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # "request":is passed so that it can be used by the template 
    # (some templates may need access to request information, such as the user's IP address, etc)
    return templates.TemplateResponse("test.html", {"request": request, "message": "nwHacks2025"})


