import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Available ENV Keys:", list(os.environ.keys()))  # Debug print

OPENROUTER_API_KEY = os.getenv(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) or os.environ.get(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)

print("🔍 Detected OPENROUTER_API_KEY:", "SET" if OPENROUTER_API_KEY else "MISSING")  # Debug print

if not OPENROUTER_API_KEY:
    raise EnvironmentError("Missing OPENROUTER_API_KEY. Set it in your Railway project settings.")
