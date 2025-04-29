from openai import OpenAI
from config import OPENROUTER_API_KEY
from dotenv import load_dotenv
import random
import time
import os

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# List of free and reliable models
FREE_MODELS = [
    "meta-llama/llama-4-scout:free",  # Very fast
    "meta-llama/llama-4-maverick:free",
    "deepseek/deepseek-r1:free",      # Slower
    "moonshotai/kimi-vl-a3b-thinking:free"
]


def smart_generate(system_prompt, user_prompt, max_retries=3):
    attempts = 0
    last_exception = None

    while attempts < max_retries:
        try:
            model_choice = random.choice(FREE_MODELS)
            print(f"[Model Fallback] Trying model: {model_choice}")

            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )

            # Log the successful model usage
            log_model_usage(model_choice)

            return response.choices[0].message.content

        except Exception as e:
            print(f"[Model Fallback] Error with {model_choice}: {e}")
            last_exception = e
            attempts += 1
            time.sleep(2)  # Wait a bit before retrying

    raise Exception(f"All model retries failed. Last error: {last_exception}")

def log_model_usage(model_name):
    log_dir = "storage"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "model_usage.log")
    with open(log_file, "a") as f:
        f.write(f"Model used: {model_name}\n")
