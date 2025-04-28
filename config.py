from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
