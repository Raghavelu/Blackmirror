# core/utils.py
import re

def sanitize_text(text):
    """Universal text cleaner for all content generation"""
    # Remove invalid Unicode ranges
    text = re.sub(r'[^\x00-\x7F\u00A0-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]', '', text)
    
    # Replace problematic characters
    replacements = {
        '\x9c': '',  # STRING TERMINATOR character
        '\u2013': '-', '\u2014': '--',
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Force valid UTF-8 encoding
    return text.encode('utf-8', 'replace').decode('utf-8')
