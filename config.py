import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Available ENV Keys:", list(os.environ.keys()))  # Debug print

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("🔍 Detected OPENROUTER_API_KEY:", "SET" if OPENROUTER_API_KEY else "MISSING")  # Debug print

if not OPENROUTER_API_KEY:
    raise EnvironmentError("Missing OPENROUTER_API_KEY. Set it in your Railway project settings.")
