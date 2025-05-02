import re

def sanitize_text(text):
    """Ultimate text sanitization with multiple fallbacks"""
    # Convert to bytes and back to clean binary artifacts
    text = text.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
    
    # Remove invalid Unicode characters
    text = re.sub(r'[^\x00-\x7F\u00A0-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', text)
    
    # Explicitly remove problematic control characters
    control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160)))
    control_chars = control_chars.replace('\n', '').replace('\t', '')
    text = text.translate(str.maketrans('', '', control_chars))
    
    # Force valid UTF-8 with replacement
    return text.encode('utf-8', 'replace').decode('utf-8')
