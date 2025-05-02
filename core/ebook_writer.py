from fpdf import FPDF
from core.deployer import extract_title
from utils.models_fallback import smart_generate
import os
import textwrap
from datetime import datetime

def sanitize_pdf_text(text):
    # ... (keep existing sanitize_pdf_text implementation) ...

def generate_ebook_content(insight_text):
    # ... (keep existing generate_ebook_content implementation) ...

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
        
        # Configure safe rendering
        pdf.set_font("Arial", size=12)
        pdf.set_doc_option('core_fonts_encoding', 'utf-8')
    
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
            pdf.cell(0, 8, f"{idx+1}. {chapter[8:].strip()}", 0, 1)

        # Main Content with Safe Wrapping
        paragraphs = [p.strip() for p in full_content.split('\n\n')]
        for para in paragraphs:
            if para.startswith('Chapter'):
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, 10, para.strip(), 0, 1)
                pdf.set_font('Arial', '', 12)
            else:
                wrapped = textwrap.wrap(para, width=100)
                for line in wrapped:
                    try:
                        pdf.multi_cell(0, 8, line)
                    except:
                        pdf.multi_cell(0, 8, line.encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(5)

        pdf.output(filename)
        
        # Validate PDF after generation
        if not validate_pdf(filename):
            raise ValueError("Generated PDF is invalid")
            
        print(f"[eBook Writer] Generated {filename} ({pdf.page_no()} pages)")
        return filename
        
    except Exception as e:
        print(f"[ERROR] Failed to generate eBook: {str(e)}")
        raise
