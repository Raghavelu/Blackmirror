import re
from datetime import datetime

def generate_upload_summary(insight_text):
    print("[Upload Summary] Creating platform-ready summary...")
    
    def extract(pattern):
        match = re.search(f"{pattern}:\s*(.+?)\n\n", insight_text, re.DOTALL)
        return match.group(1).strip() if match else "N/A"
    
    title = extract_title(insight_text).replace('_', ' ')
    price_range = re.search(r"Recommended Price: (.+)", insight_text).group(1)
    
    summary = f"""---MARKETING COPY---
Title: {title}
Description: {extract('Description')}
Audience: {extract('Target Audience')}
Price: {price_range}
Format: {extract('Format')}
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
