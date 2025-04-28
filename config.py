import os
from dotenv import load_dotenv

load_dotenv()  # This loads environment variables from a .env file

# Check if the API key is loaded correctly
api_key = os.getenv('OPENROUTER_API_KEY')
if not api_key:
    print("[ERROR] API key is missing. Please check your environment settings.")
else:
    print("[INFO] API key loaded successfully.")
