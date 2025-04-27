import json
import os

def save_log(chaos_text, insight_text, txt_file, pdf_file):
    print("[Deployer] Saving log...")

    os.makedirs('data', exist_ok=True)
    logs_file = 'data/chaos_logs.json'

    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append({
        "chaos": chaos_text,
        "insight": insight_text,
        "txt_product": txt_file,
        "pdf_product": pdf_file
    })

    with open(logs_file, 'w') as f:
        json.dump(logs, f, indent=2)
