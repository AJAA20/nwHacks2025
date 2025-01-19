from fastapi import FastAPI, UploadFile, File, HTTPException
import httpx
import os
from dotenv import load_dotenv

# Specify the path to your credential.env file
env_file = 'credential.env'

# Load environment variables from the credential.env file
load_dotenv(dotenv_path=env_file)

# Initialize FastAPI app
app = FastAPI()

# Instagram Graph API credentials from .env file
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")

# Base URL for Instagram Graph API
BASE_URL = f"https://graph.instagram.com/{INSTAGRAM_USER_ID}/media"

# Function to upload video to Instagram
async def upload_to_instagram(video_url: str):
    # Step 1: Create a media container for the video
    params = {
        'media_type': 'VIDEO',
        'video_url': video_url,
        'access_token': INSTAGRAM_ACCESS_TOKEN
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create media container.")

    media_id = response.json().get("id")
    
    # Step 2: Publish the media
    publish_url = f"https://graph.instagram.com/{INSTAGRAM_USER_ID}/media_publish"
    publish_params = {
        'creation_id': media_id,
        'access_token': INSTAGRAM_ACCESS_TOKEN
    }
    
    async with httpx.AsyncClient() as client:
        publish_response = await client.post(publish_url, params=publish_params)

    if publish_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to publish media.")
    
    return {"message": "Video posted successfully."}

# Route to upload video
@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # Save the file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Upload the video to a hosting platform (e.g., S3, Firebase, etc.) and get the URL
    # For simplicity, we will simulate this step by using the local file path as the URL
    # In production, you should upload the video to a cloud storage provider (like AWS S3) 
    # and get a publicly accessible URL.
    
    video_url = f"http://your_storage_url/{file_path}"

    # Upload the video to Instagram
    return await upload_to_instagram(video_url)

