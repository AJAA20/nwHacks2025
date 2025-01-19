import os
from dotenv import load_dotenv, set_key

# Load environment variables from .env
load_dotenv()

# Define the path to your .env file
env_file = 'credentials.env'

def save_credentials_to_env(access_token: str, user_id: str):
    """
    Store the user's access token and user ID in the .env file.
    """
    # Set the credentials in the .env file
    set_key(env_file, "INSTAGRAM_ACCESS_TOKEN", access_token)
    set_key(env_file, "INSTAGRAM_USER_ID", user_id)

    print("Credentials saved successfully!")