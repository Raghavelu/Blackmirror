import os
import re
from core.deployer import extract_title

def clean_content(text):
    # Preserve basic structure while removing problematic characters
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Convert bold to plain
    text = re.sub(r'`(.+?)`', r'\1', text)        # Remove code formatting
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Remove links but keep text
    return text.strip()

def create_assets(insight_text):
    print("[Asset Generator] Creating TXT summary...")
    os.makedirs('assets/products', exist_ok=True)
    
    base_filename = extract_title(insight_text)
    txt_path = f'assets/products/{base_filename}.txt'
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        cleaned_content = clean_content(insight_text)
        f.write(cleaned_content)
    
    print(f"[Asset Generator] Saved TXT: {txt_path}")
    return txt_path
