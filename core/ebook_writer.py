from fpdf import FPDF
from core.deployer import extract_title
from utils.models_fallback import smart_generate
import os

def generate_ebook_content(insight_text):
    system_prompt = """Expand this product concept into a comprehensive 80-100 page eBook. Structure should include:
1. Title Page
2. Table of Contents
3. 10 Chapters with 3-5 sub-sections each
4. Case Studies
5. Actionable Worksheets
6. Resource Appendix
7. About the Author

Make content professional yet engaging. Include practical examples and data where appropriate."""
    
    return smart_generate(system_prompt, insight_text)

def write_ebook(insight_text):
    print("[eBook Writer] Generating expanded eBook...")
    title = extract_title(insight_text)
    filename = f"assets/products/{title}_ebook.pdf"
    
    # Generate detailed content
    full_content = generate_ebook_content(insight_text)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 40, title, 0, 1, 'C')
    pdf.ln(20)
    
    # Table of Contents
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Table of Contents", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    chapters = [line for line in full_content.split('\n') if line.startswith('Chapter')]
    for idx, chapter in enumerate(chapters[:10]):
        pdf.cell(0, 10, f"{idx+1}. {chapter[8:].strip()}", 0, 1)
    
    # Main Content
    pdf.set_font('Arial', '', 12)
    for line in full_content.split('\n'):
        if line.startswith('Chapter'):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, line.strip(), 0, 1)
            pdf.set_font('Arial', '', 12)
        else:
            pdf.multi_cell(0, 10, line.strip())
    
    pdf.output(filename)
    print(f"[eBook Writer] Generated {filename} ({pdf.page_no()} pages)")
    return filename
