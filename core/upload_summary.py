import re
from datetime import datetime
from core.deployer import extract_title

def extract_field(pattern, text):
    try:
        match = re.search(rf"{pattern}:\s*(.+?)\n\n", text, re.DOTALL)
        return match.group(1).strip() if match else "Not specified"
    except Exception as e:
        print(f"Extraction error: {str(e)}")
        return "N/A"

def generate_upload_summary(insight_text):
    print("[Upload Summary] Creating platform-ready summary...")
    
    title = extract_title(insight_text).replace('_', ' ')
    price_range = extract_field(r"Recommended Price", insight_text)
    
    summary = f"""---MARKETING COPY---
Title: {title}
Description: {extract_field('Description', insight_text)}
Audience: {extract_field('Target Audience', insight_text)}
Price: {price_range}
Format: {extract_field('Format', insight_text)}
Release Date: {datetime.now().strftime('%Y-%m-%d')}
Tags: {', '.join(re.findall(r'\b\w+\b', title)[:5])}

---CONTENT DETAILS---
Word Count: {len(insight_text.split())}
Sections: {len(re.findall(r'## ', insight_text))}
Worksheets: {2 if 'Toolkit' in insight_text else 1}
"""

    filename = f"assets/products/{extract_title(insight_text)}_summary.txt"
    with open(filename, 'w') as f:
        f.write(summary)
    
    return filename
