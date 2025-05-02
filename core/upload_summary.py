import re
from core.deployer import extract_title
from core.utils import sanitize_text

def generate_upload_summary(insight_text):
    print("[Upload Summary] Creating platform summary...")
    clean_text = sanitize_text(insight_text)
    
    def extract(pattern):
        match = re.search(rf"{pattern}:\s*(.+?)\n\n", clean_text, re.DOTALL)
        return match.group(1).strip() if match else "N/A"
    
    title = sanitize_text(extract_title(clean_text).replace('_', ' '))
    price = re.search(r"Recommended Price:\s*(.+)", clean_text)
    
    summary = f"""Title: {title}
Description: {extract('Description')}
Audience: {extract('Target Audience')}
Price: {price.group(1) if price else '$19'}
Format: {extract('Format')}
Pages: {len(clean_text.split()) // 300}"""  # Approximate pages

    filename = f"assets/products/{extract_title(clean_text)}_summary.txt"
    with open(filename, 'w', encoding='utf-8', errors='replace') as f:
        f.write(summary)
    
    return filename
