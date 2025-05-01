import json
import os
import zipfile
import re
from datetime import datetime

LOG_FILE = 'data/chaos_logs.json'


def slugify(title):
    title = title.lower()
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[\s_-]+', '_', title).strip('_')
    return title


def extract_title(insights_text):
    patterns = [
        r'^Title:\s*["“”]?(.*?)[“”"]?\s*$',
        r'Title:\s*["“”]?(.*?)[“”"]?(?:\n|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, insights_text, re.MULTILINE)
        if match:
            return slugify(match.group(1))
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
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

    print(f"[Deployer] Log saved. Bundle created: {zip_path}")


def create_zip_bundle(txt_path, pdf_path, insights_text, ebook_path=None, toolkit_paths=None, summary_path=None):
    bundle_dir = 'assets/products'
    os.makedirs(bundle_dir, exist_ok=True)

    base_name = extract_title(insights_text)
    zip_path = os.path.join(bundle_dir, f"{base_name}.zip")

    with zipfile.ZipFile(zip_path, 'w') as bundle:
        bundle.write(txt_path, arcname=os.path.basename(txt_path))
        bundle.write(pdf_path, arcname=os.path.basename(pdf_path))
        if ebook_path:
            bundle.write(ebook_path, arcname=os.path.basename(ebook_path))
        if toolkit_paths:
            for path in toolkit_paths:
                bundle.write(path, arcname=os.path.basename(path))
        if summary_path:
            bundle.write(summary_path, arcname=os.path.basename(summary_path))

    return zip_path
