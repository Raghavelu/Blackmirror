import json
import os
import zipfile
from datetime import datetime

LOG_FILE = 'data/chaos_logs.json'

def save_log(chaos_text, insights, txt_path, pdf_path):
    # Check if 'data' directory exists before saving log
    if not os.path.exists('data'):
        print("[ERROR] Directory 'data' does not exist.")
    else:
        print("[INFO] Directory 'data' exists.")
        
    os.makedirs('data', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_entry = {
        "timestamp": timestamp,
        "chaos": chaos_text,
        "insights": insights,
        "txt_file": txt_path,
        "pdf_file": pdf_path,
        "zip_file": create_zip_bundle(txt_path, pdf_path, timestamp)
    }

    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"[Deployer] Log saved. Bundle created: {log_entry['zip_file']}")

def create_zip_bundle(txt_path, pdf_path, timestamp):
    bundle_dir = 'assets/products'
    os.makedirs(bundle_dir, exist_ok=True)

    zip_filename = os.path.join(bundle_dir, f"product_bundle_{timestamp}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as bundle:
        bundle.write(txt_path, arcname=os.path.basename(txt_path))
        bundle.write(pdf_path, arcname=os.path.basename(pdf_path))
    return zip_filename
