from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests
import os
from dotenv import load_dotenv

# Load environment variables from credentials.env
load_dotenv(dotenv_path="credentials.env")

# Create a FastAPI app
app = FastAPI()

# Instagram App credentials (stored in .env file)
CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID")
CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET")
REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI")
ENV_FILE = "credentials.env"

# Step 1: Redirect user to Instagram OAuth
@app.get("/auth/instagram/")
def instagram_login():
    authorization_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user_profile,user_media"
        f"&response_type=code"
    )
    return RedirectResponse(authorization_url)

# Step 2: Handle Instagram OAuth Callback
@app.get("/auth/instagram/callback/")
def instagram_callback(code: str):
    # Exchange authorization code for access token
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return {"error": "Failed to obtain access token."}

    token_data = response.json()
    access_token = token_data.get("access_token")
    user_id = token_data.get("user_id")

    if not access_token or not user_id:
        return {"error": "Invalid token data received."}

    # Save credentials to .env file
    save_credentials_to_env(access_token, user_id)

    return {"message": "Access token obtained and saved successfully."}

# Helper function to save credentials to .env file
def save_credentials_to_env(access_token: str, user_id: str):
    with open(ENV_FILE, "a") as env_file:
        env_file.write(f"INSTAGRAM_ACCESS_TOKEN={access_token}\n")
        env_file.write(f"INSTAGRAM_USER_ID={user_id}\n")
