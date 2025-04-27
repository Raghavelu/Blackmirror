import os
from dotenv import load_dotenv

load_dotenv()

# Try to load from .env or Railway ENV directly
OPENROUTER_API_KEY = os.getenv("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")

# Fallback (Railway workaround for early loading)
if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = os.environ.get("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")
    
if not OPENROUTER_API_KEY:
    raise EnvironmentError("Missing OPENROUTER_API_KEY. Set it in your Railway project settings.")

print("🔍 OPENROUTER_API_KEY value:", OPENROUTER_API_KEY)
