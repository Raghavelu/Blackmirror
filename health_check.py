from utils.models_fallback import FREE_MODELS
import requests
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def check_model(model_name):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you hear me?"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Model '{model_name}' is reachable.")
        else:
            print(f"[FAIL] Model '{model_name}' returned error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Model '{model_name}' failed with exception: {str(e)}")

def run_health_check():
    for model in FREE_MODELS:
        check_model(model)

if __name__ == "__main__":
    run_health_check()
