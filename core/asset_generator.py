import os
import re
from core.deployer import extract_title
from core.ebook_writer import sanitize_pdf_text

def clean_content(text):
    # Preserve basic structure while removing problematic characters
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Convert bold to plain
    text = re.sub(r'`(.+?)`', r'\1', text)        # Remove code formatting
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Remove links but keep text
    return text.strip()

def create_assets(insight_text):
    print("[Asset Generator] Creating TXT summary...")
    os.makedirs('assets/products', exist_ok=True)
    
    # Add sanitization before saving
    clean_content = sanitize_pdf_text(insight_text)
    base_filename = extract_title(clean_content)
    txt_path = f'assets/products/{base_filename}.txt'
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"[Asset Generator] Saved TXT: {txt_path}")
    return txt_path
