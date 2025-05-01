from openai import OpenAI
from config import OPENROUTER_API_KEY
import time
import os
from datetime import datetime

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

MODEL_PRIORITY_LIST = [
    "meta-llama/llama-4-scout:free", 
    "meta-llama/llama-4-maverick:free",
    "deepseek/deepseek-r1:free",
    "mistralai/mistral-7b-instruct:free"
]


VALID_MODELS = ["meta-llama/llama-4-scout:free", 
                "meta-llama/llama-4-maverick:free",
                "deepseek/deepseek-r1:free",
                "mistralai/mistral-7b-instruct:free"]

def validate_models():
    for model in MODEL_PRIORITY_LIST:
        if model not in VALID_MODELS:
            raise ValueError(f"Invalid model in priority list: {model}")


def smart_generate(system_prompt, user_prompt, max_retries=2):
    for model in MODEL_PRIORITY_LIST:
        for attempt in range(max_retries):
            try:
                print(f"Attempting {model} (try {attempt+1})")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000,
                    timeout=30
                )
                content = response.choices[0].message.content
                log_model_usage(model)
                return content
            except Exception as e:
                print(f"Model {model} failed: {str(e)}")
                time.sleep(1)
    
    raise Exception(f"All models failed after {max_retries} retries each")

def log_model_usage(model_name):
    log_dir = "storage"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/model_usage.log", "a") as f:
        f.write(f"{datetime.now().isoformat()}|{model_name}\n")
