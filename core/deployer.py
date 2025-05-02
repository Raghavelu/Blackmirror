import json
import os
import zipfile
import re
from datetime import datetime
from core.utils import sanitize_text

LOG_FILE = 'data/chaos_logs.json'

def slugify(title):
    title = re.sub(r'[^\w\s-]', '', title.lower())
    return re.sub(r'[\s_-]+', '_', title).strip('_')

def extract_title(insights_text):
    patterns = [
        r'(?i)^#*\s*Title\s*[:\-]?\s*["“”]?(.+?)["“”"]?$',
        r'(?im)^Title\s*:\s*["“”]?([^\n]+?)["“”"]?$'
    ]
    for pattern in patterns:
        match = re.search(pattern, insights_text)
        if match:
            return slugify(match.group(1))
    return f"product_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def save_log(chaos_text, insights, txt_path, zip_path, ebook_path, toolkit_paths):
    os.makedirs('data', exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "chaos": chaos_text,
        "assets": {
            "summary": txt_path,
            "ebook": ebook_path,
            "toolkit": toolkit_paths,
            "bundle": zip_path
        }
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            pass
    
    logs.append(log_entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"[Deployer] Log saved: {zip_path}")

def create_zip_bundle(txt_path, ebook_path, toolkit_paths, summary_path):
    base_name = extract_title(open(txt_path).read())
    zip_path = f'assets/products/{base_name}.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as bundle:
        # Mandatory files
        bundle.write(txt_path, arcname='product_summary.txt')
        bundle.write(ebook_path, arcname='full_ebook.pdf')
        bundle.write(summary_path, arcname='platform_summary.txt')
        
        # Optional toolkit
        if toolkit_paths:
            for path in toolkit_paths:
                bundle.write(path, arcname=f'toolkit/{os.path.basename(path)}')
    
    return zip_path
