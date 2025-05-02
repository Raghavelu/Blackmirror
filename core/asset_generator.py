import os
from core.deployer import extract_title
from core.utils import sanitize_text

def create_assets(insight_text):
    print("[Asset Generator] Creating TXT summary...")
    os.makedirs('assets/products', exist_ok=True)
    
    clean_content = sanitize_text(insight_text)
    base_filename = extract_title(clean_content)
    txt_path = f'assets/products/{base_filename}.txt'
    
    with open(txt_path, 'w', encoding='utf-8', errors='replace') as f:
        f.write(clean_content)
    
    print(f"[Asset Generator] Saved TXT: {txt_path}")
    return txt_path
