from fpdf import FPDF
from core.deployer import extract_title
from utils.models_fallback import smart_generate
import os
import textwrap
from datetime import datetime

def sanitize_pdf_text(text):
    # Replace problematic Unicode characters
    replacements = {
        '\u2013': '-', 
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove control characters
    return ''.join(c for c in text if ord(c) >= 32 or ord(c) == 10)

def generate_ebook_content(insight_text):
    system_prompt = """Expand this product concept into a comprehensive 80-100 page eBook. Structure should include:
1. Title Page
2. Table of Contents
3. 10 Chapters with 3-5 sub-sections each
4. Case Studies
5. Actionable Worksheets
6. Resource Appendix
7. About the Author"""
    
    return smart_generate(system_prompt, insight_text)

def validate_pdf(path):
    try:
        with open(path, 'rb') as f:
            return f.read(4) == b'%PDF'
    except:
        return False

def write_ebook(insight_text):
    try:
        print("[eBook Writer] Generating expanded eBook...")
        title = extract_title(insight_text)
        filename = f"assets/products/{title}_ebook.pdf"
        
        full_content = generate_ebook_content(insight_text)
        full_content = sanitize_pdf_text(full_content)
    
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        pdf.add_page()
        
        # Configure safe rendering with explicit dimensions
        pdf.set_font("Arial", size=12)
        pdf.set_doc_option('core_fonts_encoding', 'utf-8')
        effective_page_width = pdf.w - 2*pdf.l_margin  # Calculate available width

        # Title Page
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 40, title, 0, 1, 'C')
        pdf.ln(30)

        # Table of Contents
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Table of Contents", 0, 1)
        pdf.set_font('Arial', '', 12)
        
        chapters = [line for line in full_content.split('\n') if line.startswith('Chapter')]
        for idx, chapter in enumerate(chapters[:10]):
            safe_text = chapter[8:].strip().encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 8, f"{idx+1}. {safe_text}", 0, 1)

        # Main Content with Safe Wrapping
        paragraphs = [p.strip() for p in full_content.split('\n\n')]
        for para in paragraphs:
            if para.startswith('Chapter'):
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, 10, para.strip(), 0, 1)
                pdf.set_font('Arial', '', 12)
            else:
                # Use calculated page width for wrapping
                wrapped = textwrap.wrap(para, width=int(effective_page_width/2.5))  # ~80 chars
                for line in wrapped:
                    try:
                        # Use explicit width for multi_cell
                        pdf.multi_cell(effective_page_width, 8, line)
                    except Exception as e:
                        # Fallback rendering
                        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(effective_page_width, 8, safe_line)
                pdf.ln(5)

        pdf.output(filename)
        
        if not validate_pdf(filename):
            raise ValueError("Generated PDF is invalid")
            
        print(f"[eBook Writer] Generated {filename} ({pdf.page_no()} pages)")
        return filename
        
    except Exception as e:
        print(f"[ERROR] Failed to generate eBook: {str(e)}")
        raise
