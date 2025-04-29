import json
import os
import zipfile
import re
from datetime import datetime

LOG_FILE = 'data/chaos_logs.json'

def slugify(title):
    """Convert product title to safe filename"""
    title = title.lower()
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[\s_-]+', '_', title).strip('_')
    return title


def extract_title(insights_text):
    """Extracts a clean title from GPT output"""
    # Try to match Title: "..." or Title: ...
    patterns = [
        r'^Title:\s*["“”]?(.*?)["“”]?\s*$',
        r'Title:\s*["“”]?(.*?)["“”]?(?:\n|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, insights_text, re.MULTILINE)
        if match:
            return slugify(match.group(1))

    # Fallback title
    return f"blackmirror_product_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def save_log(chaos_text, insights, txt_path, pdf_path, zip_path):
    os.makedirs('data', exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_entry = {
        "timestamp": timestamp,
        "chaos": chaos_text,
        "insights": insights,
        "txt_file": txt_path,
        "pdf_file": pdf_path,
        "zip_file": zip_path
    }

    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"[Deployer] Log saved. Bundle created: {zip_path}")


def create_zip_bundle(txt_path, pdf_path, title_text):
    bundle_dir = 'assets/products'
    os.makedirs(bundle_dir, exist_ok=True)

    base = extract_title(title_text)
    zip_filename = os.path.join(bundle_dir, f"{base}.zip")

    with zipfile.ZipFile(zip_filename, 'w') as bundle:
        bundle.write(txt_path, arcname=os.path.basename(txt_path))
        bundle.write(pdf_path, arcname=os.path.basename(pdf_path))

    return zip_filename
