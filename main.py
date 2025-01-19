# from typing import Union
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from starlette.requests import Request # to get the request context

# # https://fastapi.tiangolo.com/#example
# app = FastAPI() # Creates an instance of FastAPI, assigning it to the variable `app`

# '''
# This object manages the template loading and rendering process. By passing
# "templates" to the directory argument, we're telling FastAPI that the
# HTML files (like test.html) are located in a folder called templates to where
# app.py is located
# '''
# templates = Jinja2Templates(directory="templates") 

# # decorator that binds read_root to GET request to the root
# # when a user accesses http://localhost:8000/, this function is triggered 
# # By default, FastAPI returns JSON responses, but since we're rendering an HTML page
# # we specify that the response should be of type HTMLResponse.
# # This tells FastAPI to send HTML content back to the client, rather than JSON.
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     # "request":is passed so that it can be used by the template 
#     # (some templates may need access to request information, such as the user's IP address, etc)
#     return templates.TemplateResponse("test.html", {"request": request, "message": "nwHacks2025"})

# @app.get("/post", response_class=HTMLResponse)
# async def read_post(request: Request):
#     return templates.TemplateResponse("post.html", {"request": request})

# @app.get("/login", response_class=HTMLResponse)
# async def read_login(request: Request):
#     return templates.TemplateResponse("loginpage.html", {"request": request})


'''
TRYING TO USE YOUTUBE API !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''

from typing import Union
from fastapi import FastAPI, Form
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from googleapiclient.http import MediaFileUpload  # <-- Added this import
import google_auth_oauthlib
from starlette.requests import Request # to get the request context
from google.oauth2.credentials import Credentials # For handling OAuth 2.0 credentials
from google.auth.transport.requests import Request as GoogleRequest # HTTP requests for OAuth2
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build # to interact with the youtube api
import os
import json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# https://fastapi.tiangolo.com/#example
app = FastAPI() # Creates an instance of FastAPI, assigning it to the variable `app`

'''
This object manages the template loading and rendering process. By passing
"templates" to the directory argument, we're telling FastAPI that the
HTML files (like test.html) are located in a folder called templates to where
app.py is located
'''
templates = Jinja2Templates(directory="templates") 

# this is the OAuth2 client ID and secret file generated from the Google Developer Console
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Store credentials globally for simplicity
credentials = None

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

@app.get("/post", response_class=HTMLResponse)
async def read_post(request: Request):
    return templates.TemplateResponse("post.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("loginpage.html", {"request": request})

@app.get("/get", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("post_example.html", {"request": request})

@app.post("/submit")
async def post_message(message: str = Form(...)):
    return {"response": f"Server recieved your message: {message}"}

@app.get("/loginyt", response_class=HTMLResponse)
async def login_yt(request: Request):
    # This renders the loginyt.html page when the user accesses /loginyt
    return templates.TemplateResponse("loginyt.html", {"request": request})

@app.get("/auth/google")
async def google_auth(request: Request):
    # redirects user to Google OAuth login page

    # redirect URI should match what we have in Google Developer Console settings
    redirect_uri = "http://localhost:8000/auth/google/callback"

    # send the user to the Google OAuth page
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = redirect_uri

    # part of the OAuth 2.0 authorization flow and is used to 
    # generate the authorization URL that the user will be redirected 
    # to in order to authenticate and authorize the application to access 
    # their Google account (in this case, YouTube)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scope='true')
    
    return {"authorization_url": authorization_url}

@app.get("/auth/google/callback")
async def google_callback(request: Request, code: str):
    # Allow insecure transport for local testing
    import os
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    global credentials

    # Initialize the OAuth flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = "http://localhost:8000/auth/google/callback"

    try:
        # Exchange the authorization code for credentials
        flow.fetch_token(authorization_response=str(request.url))

        # Extract the credentials from the flow object
        credentials = flow.credentials

        # Convert the credentials to a dictionary for JSON response
        credentials_dict = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        return RedirectResponse(url="/uploadyt")

    except Exception as e:
        # Handle errors and return the error message
        return {"message": "Failed to authenticate", "error": str(e)}
    

@app.get("/uploadyt", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Renders the upload video page."""
    # Ensure user is authenticated
    if not credentials:
        return {"message": "You need to login first."}
    
    return templates.TemplateResponse("uploadyt.html", {"request": request})


@app.post("/upload")
async def upload_video(
    title: str = Form(...),
    description: str = Form(...),
    videoFile: UploadFile = File(...),
    request: Request = None,
):
    """Handles video upload to YouTube."""
    if not credentials:
        raise HTTPException(status_code=401, detail="You need to log in first")

    # Save the uploaded file temporarily
    temp_video_path = f"temp_{videoFile.filename}"
    with open(temp_video_path, "wb") as buffer:
        buffer.write(await videoFile.read())

    try:
        # Initialize YouTube API client
        youtube = build("youtube", "v3", credentials=credentials)

        # Create media upload object
        media = MediaFileUpload(temp_video_path, chunksize=-1, resumable=True)
        
        # Create video resource body
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["example", "upload"],
                    "categoryId": "22"  # Category for "People & Blogs"
                },
                "status": {
                    "privacyStatus": "private"  # You can set this to "public" or "unlisted"
                }
            },
            media_body=media
        )

        # Execute upload
        response = request.execute()

        # Clean up temporary file
        os.remove(temp_video_path)

        return {"message": "Video uploaded successfully!", "video": response}

    except Exception as e:
        return {"message": "Failed to upload video", "error": str(e)}

