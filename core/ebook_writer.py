# core/ebook_writer.py
from fpdf import FPDF
from core.deployer import extract_title
from utils.models_fallback import smart_generate
import os
import textwrap
from datetime import datetime

# --------------------------
# TEXT SANITIZATION UTILITIES
# --------------------------
def sanitize_pdf_text(text):
    """Multi-layer text sanitization with byte-level cleaning"""
    # Layer 1: Force valid UTF-8 with multiple fallbacks
    try:
        text = text.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError:
        text = text.encode('utf-8', 'replace').decode('utf-8')
    except UnicodeEncodeError:
        text = text.encode('latin-1', 'replace').decode('latin-1')
    
    # Layer 2: Replace problematic Unicode characters
    replacements = {
        '\u2013': '-', '\u2014': '--',
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u00a0': ' ',
        '\u200b': '', '\ufffd': '(?)'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Layer 3: Remove remaining non-printable characters
    return ''.join(c for c in text if 31 < ord(c) < 127 or c in ('\n', '\t'))

# ---------------------------
# CONTENT GENERATION SECTION
# ---------------------------
def generate_ebook_content(insight_text):
    """Generate expanded eBook content using AI model"""
    system_prompt = """Expand this product concept into a comprehensive 80-100 page eBook. Structure must include:
1. Title Page
2. Table of Contents
3. 10 Chapters with 3-5 sub-sections each
4. Case Studies
5. Actionable Worksheets
6. Resource Appendix
7. About the Author"""
    
    return smart_generate(system_prompt, insight_text)

# ------------------------
# PDF VALIDATION UTILITIES
# ------------------------
def validate_pdf(path):
    """Robust PDF validation with content check"""
    try:
        with open(path, 'rb') as f:
            # Check header
            if f.read(4) != b'%PDF':
                return False
            
            # Check basic structure
            f.seek(0)
            content = f.read(4096)
            if b'%%EOF' not in content:
                # Full file scan for EOF marker
                f.seek(-1024, 2)
                if b'%%EOF' not in f.read():
                    return False
            
            return True
    except Exception as e:
        print(f"PDF Validation Error: {str(e)}")
        return False

# ----------------------
# MAIN EBOOK GENERATION
# ----------------------
def write_ebook(insight_text):
    """Generate full eBook PDF with error handling"""
    try:
        print("[eBook Writer] Starting generation...")
        title = extract_title(insight_text)
        filename = f"assets/products/{title}_ebook.pdf"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Generate and sanitize content
        raw_content = generate_ebook_content(insight_text)
        clean_content = sanitize_pdf_text(raw_content)
        
        if not clean_content:
            raise ValueError("Generated content is empty")

        # Initialize PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        effective_width = pdf.w - 2*pdf.l_margin  # Page width minus margins

        # --------------------------
        # SAFE CONTENT ADDITION SYSTEM
        # --------------------------
        def safe_add(text, font_size=12, style=''):
            """Universal safe text addition with wrapping"""
            pdf.set_font('Arial', style, font_size)
            text = sanitize_pdf_text(str(text))
            
            # Split into paragraphs
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                # Split into lines with width calculation
                wrapped = textwrap.wrap(para, width=int(effective_width/4.5))  # ~80 chars
                for line in wrapped:
                    # Final safety layer
                    try:
                        pdf.multi_cell(effective_width, 10, line)
                    except:
                        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(effective_width, 10, safe_line)
                pdf.ln(4)  # Paragraph spacing

        # --------------------------
        # EBOOK STRUCTURE BUILDING
        # --------------------------
        # Title Page
        pdf.add_page()
        safe_add(title, font_size=24, style='B')
        pdf.ln(30)
        safe_add(f"Generated: {datetime.now().strftime('%Y-%m-%d')}", 14)

        # Table of Contents
        pdf.add_page()
        safe_add("Table of Contents", 16, 'B')
        chapters = [line for line in clean_content.split('\n') if line.startswith('Chapter')]
        for idx, chapter in enumerate(chapters[:10]):
            safe_add(f"{idx+1}. {chapter[8:].strip()}", 12)

        # Main Content
        sections = clean_content.split('\n\n')
        for section in sections:
            if section.startswith('Chapter'):
                pdf.add_page()
                safe_add(section.strip(), 16, 'B')
            else:
                safe_add(section, 12)

        # Finalize and validate
        pdf.output(filename)
        if not validate_pdf(filename):
            raise ValueError("PDF failed validation checks")
            
        print(f"[eBook Writer] Success: {filename} ({pdf.page_no()} pages)")
        return filename

    except Exception as e:
        print(f"[CRITICAL ERROR] eBook Generation Failed: {str(e)}")
        raise
